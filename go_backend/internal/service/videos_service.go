package service

import (
	"fmt"
	"go_backend/internal/repository/interfaces"
	"go_backend/internal/schemas"
)

type VideoService struct {
	sqlRepo   interfaces.PostgresRepository
	redisRepo interfaces.RedisRepository
	cacheRepo interfaces.CacheRepository
}

func NewVideoService(
	sqlRepo interfaces.PostgresRepository,
	redisRepo interfaces.RedisRepository,
	cacheRepo interfaces.CacheRepository,
) *VideoService {

	return &VideoService{
		sqlRepo:   sqlRepo,
		redisRepo: redisRepo,
		cacheRepo: cacheRepo,
	}
}

func (serv *VideoService) IsVideoExists(taskID string) (bool, string, error) {
	data, exists, err := serv.sqlRepo.GetRowWithID(taskID)
	if err != nil {
		return false, "", fmt.Errorf("unexpected error on getting task, %w", err)
	}
	if !exists {
		return false, "", nil
	}
	return true, data.Status, nil
}

func (serv *VideoService) GetVideoFromSQL(taskID string) (schemas.VideoData, error) {
	data, exists, err := serv.sqlRepo.GetRowWithID(taskID)
	if err != nil {
		return schemas.VideoData{}, fmt.Errorf("unexpected error on getting task, %w", err)
	}
	if !exists {
		return schemas.VideoData{}, fmt.Errorf("task doesnt exists, %w", err)
	}
	return data, nil
}

func (serv *VideoService) GetVideoData(videoID string) (schemas.VideoData, bool, error) {
	video, exists, err := serv.cacheRepo.GetVideo(videoID)
	if err == nil && exists {
		return video, true, nil
	}
	video, exists, err = serv.sqlRepo.GetRowWithID(videoID)
	if err != nil {
		return schemas.VideoData{}, false, fmt.Errorf("error on getting video from db, %w", err)
	}
	if !exists {
		return schemas.VideoData{}, false, nil
	}

	if video.Status == "done" {
		serv.cacheRepo.SetVideo(videoID, video)
	}
	return video, true, nil
}

func (serv *VideoService) AddVideoToDatabase(data schemas.VideoData) error {
	err := serv.sqlRepo.InsertRow(data)
	if err != nil {
		return fmt.Errorf("error on inserting data, %w", err)
	}
	return nil
}

func (serv *VideoService) AddVideoToQueue(id, link string) error {
	added, err := serv.redisRepo.AddTask(id, link)
	if err != nil {
		return fmt.Errorf("error on adding task, %w", err)
	}
	if !added {
		return fmt.Errorf("error on adding task, %w", err)
	}
	return nil
}
