package redisRepository

import (
	"context"
	"fmt"
	"go_backend/internal/repository/interfaces"

	"github.com/redis/go-redis/v9"
)

type redisRepo struct {
	DB *redis.Client
}

func CreateNewRepo(rdb *redis.Client) interfaces.RedisRepository {
	return &redisRepo{
		DB: rdb,
	}
}

var addScript = redis.NewScript(`
if #KEYS ~= 0 then
	error("No keys expected")
end
local is_exist = redis.call("HEXISTS", "hash", ARGV[1])
if is_exist == 1 then
	return 0
end
redis.call("RPUSH", "queue", ARGV[1])
redis.call("HSET", "hash", ARGV[1], ARGV[2])
return 1
`)

func (rep *redisRepo) IsTaskInQueue(key, id string) (bool, error) {
	result := rep.DB.HExists(context.Background(), key, id)
	exists, err := result.Result()

	if err != nil {
		err = fmt.Errorf("redis script evaluating error")
		return false, err
	}
	return exists, nil
}

func (rep *redisRepo) AddTask(id string, link string) (bool, error) {
	result := addScript.Run(context.Background(), rep.DB, []string{}, []interface{}{id, link})
	added, err := result.Result()

	if err != nil {
		switch {
		case redis.HasErrorPrefix(err, "NOSCRIPT"):
			err = fmt.Errorf("NOSCRIPT")
		default:
			err = fmt.Errorf("redis script evaluating error")
		}
		return false, err
	}
	addedInt, ok := added.(int64)
	if !ok {
		return false, fmt.Errorf("unexpected result type: %T", added)
	}
	return addedInt == 1, nil
}
