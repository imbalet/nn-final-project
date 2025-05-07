package postgresRepository

import (
	"database/sql"
	"errors"
	"fmt"
	"go_backend/internal/repository/interfaces"
	"go_backend/internal/schemas"
	"go_backend/internal/utils"
	"log"
	"strings"

	"github.com/lib/pq"
)

type postgresRepo struct {
	DB       *sql.DB
	table    string
	idColumn string
}

func CreateNewRepo(sqlDB *sql.DB, table, idColumn string) interfaces.PostgresRepository {
	return &postgresRepo{
		DB:       sqlDB,
		table:    table,
		idColumn: idColumn,
	}
}

func (rep *postgresRepo) GetRowWithID(id string) (schemas.VideoData, bool, error) {
	quotedTable := pq.QuoteIdentifier(rep.table)
	quotedIdColumn := pq.QuoteIdentifier(rep.idColumn)

	query := fmt.Sprintf(
		"SELECT * FROM %s WHERE %s = $1",
		quotedTable,
		quotedIdColumn,
	)

	row := rep.DB.QueryRow(query, id)

	data := schemas.VideoData{}

	err := row.Scan(&data.Id, &data.Summary, &data.PreviewLink, &data.Title, &data.Status, &data.CreatedAt)
	if err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return schemas.VideoData{}, false, nil
		}
		return schemas.VideoData{}, false, fmt.Errorf("unexpected postgres error %w", err)
	}
	return data, true, nil
}

func (rep *postgresRepo) InsertRow(data schemas.VideoData) error {
	columns, values, err := utils.GetStructFields(data, "db")
	if err != nil {
		return fmt.Errorf("error in passed struct, %w", err)
	}

	quotedTable := pq.QuoteIdentifier(rep.table)
	quotedColumns := make([]string, len(columns))
	for i, col := range columns {
		quotedColumns[i] = pq.QuoteIdentifier(col)
	}

	placeholders := make([]string, len(values))
	for i := range placeholders {
		placeholders[i] = fmt.Sprintf("$%d", i+1)
	}

	setStatements := make([]string, 0, len(columns))
	for _, col := range columns {
		setStatements = append(setStatements, fmt.Sprintf("%s = EXCLUDED.%s", col, col))
	}

	query := fmt.Sprintf(`
        INSERT INTO %s (%s)
        VALUES (%s)
        ON CONFLICT (%s) 
        DO UPDATE SET %s`,
		quotedTable,
		strings.Join(columns, ", "),
		strings.Join(placeholders, ", "),
		rep.idColumn,
		strings.Join(setStatements, ", "),
	)

	_, err = rep.DB.Exec(query, values...)
	return err
}

func (rep *postgresRepo) UpdateRow(data schemas.Result) error {
	columns, values, err := utils.GetStructFields(data, "db")

	var filteredColumns []string
	var filteredValues []interface{}

	for i := 0; i < len(values); i++ {
		val := values[i]
		if val != "" {
			filteredValues = append(filteredValues, val)
			filteredColumns = append(filteredColumns, columns[i])
		}
	}

	if len(filteredColumns) == 0 {
		return fmt.Errorf("no non-empty fields to update")
	}
	columns = filteredColumns
	values = filteredValues

	if err != nil {
		return fmt.Errorf("error in passed struct, %w", err)
	}
	var newVals []string

	for i := 0; i < len(values); i++ {
		newVals = append(newVals, fmt.Sprintf("%s = $%d", pq.QuoteIdentifier(columns[i]), i+1))
	}
	query := fmt.Sprintf(
		"UPDATE %s SET %s WHERE %s = $%d",
		rep.table,
		strings.Join(newVals, ", "),
		rep.idColumn,
		len(columns)+1)

	args := append(values, data.Id)

	res, err := rep.DB.Exec(query, args...)
	count, _ := res.RowsAffected()
	if count != 1 {
		log.Printf("unexpected rows count affected, expected 1, affected %d", count)
	}
	return err
}
