package main

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"go_backend/internal/handler"
	"go_backend/internal/repository/cacheRepository"
	"go_backend/internal/repository/interfaces"
	"go_backend/internal/repository/postgresRepository"
	"go_backend/internal/repository/redisRepository"
	"go_backend/internal/schemas"
	"go_backend/internal/service"
	"go_backend/pkg/database"
	"log"
	"net/http"
	"os"
	"strconv"
	"time"

	"github.com/joho/godotenv"
	"github.com/redis/go-redis/v9"
)

func init() {
	if err := godotenv.Load(); err != nil {
		panic("No .env file found")
	}
}

func initRedis() *redis.Client {
	redisHost, exists := os.LookupEnv("REDIS_HOST")
	if !exists {
		panic("REDIS_HOST is not exists")
	}

	redisPortStr, exists := os.LookupEnv("REDIS_PORT")
	if !exists {
		panic("REDIS_PORT is not exists")
	}
	redisPort, err := strconv.Atoi(redisPortStr)
	if err != nil {
		log.Panicf("Failed to parse REDIS_PORT: %v", err.Error())
	}

	redisPassword, exists := os.LookupEnv("REDIS_PASSWORD")
	if !exists {
		panic("REDIS_PASSWORD is not exists")
	}

	rdb, err := database.RedisConnect(redisHost, redisPort, redisPassword)

	if err != nil {
		panic("Failed to connect to Redis: " + err.Error())
	}

	return rdb
}

func initPostgres() *sql.DB {
	postgresUsername, exists := os.LookupEnv("POSTGRES_USERNAME")
	if !exists {
		panic("POSTGRES_USERNAME is not exists")
	}

	postgresPassword, exists := os.LookupEnv("POSTGRES_PASSWORD")
	if !exists {
		panic("POSTGRES_PASSWORD is not exists")
	}

	postgresHost, exists := os.LookupEnv("POSTGRES_HOST")
	if !exists {
		panic("POSTGRES_HOST is not exists")
	}

	postgresPortStr, exists := os.LookupEnv("POSTGRES_PORT")
	if !exists {
		panic("POSTGRES_PORT is not exists")
	}
	postgresPort, err := strconv.Atoi(postgresPortStr)
	if err != nil {
		log.Panicf("Failed to parse REDIS_PORT: %v", err.Error())
	}

	postgresDatabse, exists := os.LookupEnv("POSTGRES_DATABASE")
	if !exists {
		panic("POSTGRES_DATABASE is not exists")
	}

	pdb, err := database.PostgresConnect(postgresHost, postgresPort, postgresUsername, postgresPassword, postgresDatabse)

	if err != nil {
		panic("Failed to connect to Postgres: " + err.Error())
	}
	return pdb
}

func TransferTask(rdb *redis.Client, sqlRepo interfaces.PostgresRepository) {
	for {
		result := rdb.BLPop(context.Background(), 0, "done")
		data, err := result.Result()

		if err != nil {
			log.Printf("Redis BLPop error: %v", err)
			continue
		}

		if len(data) < 2 {
			log.Println("Invalid data format from Redis")
			continue
		}

		jsonStr := data[1]

		var taskResult schemas.Result
		if err := json.Unmarshal([]byte(jsonStr), &taskResult); err != nil {
			log.Printf("JSON parse error: %v", err)
			continue
		}

		if taskResult.Status == "error" {
			log.Printf("Error on task: %+v", taskResult)
			continue
		}

		err = sqlRepo.UpdateRow(taskResult)
		if err != nil {
			log.Printf("Updating to sql error: %v", err)
			continue
		}
	}
}

func enableCORS(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

		if r.Method == "OPTIONS" {
			w.WriteHeader(http.StatusOK)
			return
		}

		next.ServeHTTP(w, r)
	}
}

func main() {
	serverPort, exists := os.LookupEnv("SERVER_PORT")
	if !exists {
		panic("SERVER_PORT is not exists")
	}

	rdb := initRedis()
	pdb := initPostgres()
	defer rdb.Close()
	defer pdb.Close()
	sqlRepo := postgresRepository.CreateNewRepo(pdb, "video", "video_id")
	redisRepo := redisRepository.CreateNewRepo(rdb)
	cacheRepo := cacheRepository.CreateNewRepo(rdb, time.Hour)

	go TransferTask(rdb, sqlRepo)

	videoService := service.NewVideoService(sqlRepo, redisRepo, cacheRepo)
	handlers := handler.NewHandlers(videoService)
	http.HandleFunc("/process", enableCORS(handlers.Process))
	http.HandleFunc("/video/", enableCORS(handlers.GetVideoData))
	http.ListenAndServe(fmt.Sprintf(":%s", serverPort), nil)

}
