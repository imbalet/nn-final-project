package interfaces

import "go_backend/internal/schemas"

type PostgresRepository interface {
	GetRowWithID(id string) (schemas.VideoData, bool, error)
	InsertRow(data schemas.VideoData) error
	UpdateRow(data schemas.Result) error
}
