package schemas

type Result struct {
	Id          string `db:"video_id" json:"id"`
	Summary     string `db:"summary" json:"summary"`
	PreviewLink string `db:"preview_link" json:"preview_link"`
	Title       string `db:"title" json:"title"`
	Status      string `db:"task_state" json:"status"`
}
