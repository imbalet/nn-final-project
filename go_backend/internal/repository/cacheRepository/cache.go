package cacheRepository

import (
	"context"
	"encoding/json"
	"fmt"
	"go_backend/internal/repository/interfaces"
	"go_backend/internal/schemas"
	"time"

	"github.com/redis/go-redis/v9"
)

type cacheRepo struct {
	rdb               *redis.Client
	defaultExpiration time.Duration
}

func CreateNewRepo(rdb *redis.Client, defaultExpiration time.Duration) interfaces.CacheRepository {
	return &cacheRepo{
		rdb: rdb, defaultExpiration: defaultExpiration,
	}
}

func (rep cacheRepo) GetVideo(id string) (schemas.VideoData, bool, error) {
	key := fmt.Sprintf("video:%s", id)
	result := rep.rdb.Get(context.Background(), key)
	value, err := result.Bytes()
	if err != nil {
		if err == redis.Nil {
			return schemas.VideoData{}, false, nil
		}
		return schemas.VideoData{}, false, fmt.Errorf("failed to get value from cache: %v", err)
	}
	video_data := schemas.VideoData{}
	if err := json.Unmarshal(value, &video_data); err != nil {
		return schemas.VideoData{}, false, fmt.Errorf("failed to unmarshal cached value: %v", err)
	}
	return video_data, true, nil
}

func (rep cacheRepo) SetVideo(id string, video schemas.VideoData) error {
	key := fmt.Sprintf("video:%s", video.Id)

	data, err := json.Marshal(video)
	if err != nil {
		return fmt.Errorf("failed to marshal value: %v", err)
	}

	if err := rep.rdb.Set(context.Background(), key, data, rep.defaultExpiration).Err(); err != nil {
		return fmt.Errorf("failed to set value in cache: %v", err)
	}
	return nil
}
