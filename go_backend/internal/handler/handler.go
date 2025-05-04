package handler

import (
	"encoding/json"
	"go_backend/internal/schemas"
	"go_backend/internal/service"
	"io"
	"net/http"
	"strings"
	"time"
)

type Handler struct {
	videoService *service.VideoService
}

func NewHandlers(videoService *service.VideoService) *Handler {
	return &Handler{videoService: videoService}
}

func (h *Handler) Process(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}
	body, err := io.ReadAll(r.Body)
	defer r.Body.Close()

	if err != nil {
		http.Error(w, "Error reading request body", http.StatusBadRequest)
		return
	}

	var data struct {
		Url string `json:"url"`
	}

	if err := json.Unmarshal(body, &data); err != nil {
		http.Error(w, "Wrong json", http.StatusBadRequest)
		return
	}

	id, found := getIdFromLink(data.Url)
	if !found {
		http.Error(w, "Wrong link passed", http.StatusBadRequest)
		return
	}

	exists, err := h.videoService.IsVideoExists(id)

	if err != nil {
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	if !exists {
		err = h.videoService.AddVideoToDatabase(schemas.VideoData{
			Id:        id,
			CreatedAt: time.Now(),
			Status:    "pending",
		})
		if err != nil {
			http.Error(w, "Internal Server Error", http.StatusInternalServerError)
			return
		}
		err = h.videoService.AddVideoToQueue(id, data.Url)
		if err != nil {
			http.Error(w, "Internal Server Error", http.StatusInternalServerError)
			return
		}
	}

	var response struct {
		Id string `json:"id"`
	}
	response.Id = id
	jsonData, err := json.Marshal(response)

	if err != nil {
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusAccepted)
	w.Header().Set("Content-Type", "application/json")
	w.Write([]byte(jsonData))
}

func (h *Handler) GetVideoData(w http.ResponseWriter, r *http.Request) {
	// /video/<id>/summary
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}
	segments := strings.Split(r.URL.Path, "/")
	if len(segments) != 4 || segments[3] != "summary" {
		http.NotFound(w, r)
		return
	}

	videoID := segments[2]

	video, exists, err := h.videoService.GetVideoData(videoID)
	if err != nil {
		http.Error(w, "Getting video error", http.StatusInternalServerError)
		return
	}
	if !exists {
		http.Error(w, "Video not exists", http.StatusNotFound)
		return
	}
	jsonData, err := json.Marshal(video)

	if err != nil {
		http.Error(w, "Getting video error", http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusOK)
	w.Header().Set("Content-Type", "application/json")
	w.Write([]byte(jsonData))
}
