package database

import (
	"database/sql"
	"fmt"
)

func PostgresConnect(host string, port int, username string, password string, dbname string) (*sql.DB, error) {
	connStr := fmt.Sprintf("postgres://%s:%s@%s:%d/%s?sslmode=disable", username, password, host, port, dbname)
	client, err := sql.Open("postgres", connStr)

	if err != nil {
		return nil, fmt.Errorf("failed to connect postgres: %w", err)
	}

	_, err = client.Exec(`
		DO $$
		BEGIN
			IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'state') THEN
				CREATE TYPE state AS ENUM ('pending', 'processing', 'done', 'error');
			END IF;
		END$$;
		CREATE TABLE IF NOT EXISTS video(
		video_id TEXT PRIMARY KEY,
		summary TEXT,
		preview_link TEXT,
		title TEXT,
		task_state state,
		created_at TIMESTAMP
		);
	`)
	if err != nil {
		return nil, fmt.Errorf("failed to create relation: %w", err)
	}

	return client, nil
}
