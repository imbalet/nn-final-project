package interfaces

import "go_backend/internal/schemas"

type CacheRepository interface {
	GetVideo(id string) (schemas.VideoData, bool, error)
	SetVideo(id string, video schemas.VideoData) error
}
