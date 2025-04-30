# Go API backend for project

## env

The app requires .env file with environment variables

```
REDIS_HOST="<host>"
REDIS_PORT="<port>"
REDIS_PASSWORD="<password>"

POSTGRES_USERNAME="<username>"
POSTGRES_PASSWORD="<password>"
POSTGRES_HOST="<host>"
POSTGRES_PORT="<port>"
POSTGRES_DATABASE="<database_name>"

SERVER_PORT="8000"
```

## Running

Run `go mod tidy` to install all dependencies

To build, execute from this directory 
```shell
go build cmd/server/main.go
```
and run `./main`


Or you can run it by 
```shell
go run cmd/server/main.go
```

Note: The .env file might need to be placed in `cmd/server/`


## API

The API includes 2 endpoints

### /video/process

**POST** method
- 202 Accepted: task accepted
- 400 Bad Request: error reading body or wrong JSON data
- 500 Internal Server Error: database query error

**Accepts** JSON body data with URL of video
```json
{
    "url": "<video_url>"
}
``` 
**Returns** task id which can be used later to request a task.
```json
{
    "id": "<id>"
}
```

### /video/\<id\>/summary

**GET** method
- 200 OK: returns data
- 404 Not Found: task not found
- 500 Internal Server Error: database query error
**Accepts** task id in the endpoint
**Returns** JSON object with task data
```json
{
    "id": "<id>",
    "summary": "<text>",
    "preview_link": "<url>",
    "title": "<text>",
    "status": "<status>",
    "created_at": "<datetime>"
}
```
`status` field can be "pending" and "done"
When status is `pending` some fields may be empty. At the end of video processing all fields will be available. 
