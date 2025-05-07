Simple project for YouTube video summarization.

---

- [Structure](#structure)
  - [General structure](#general-structure)
  - [Services interaction](#services-interaction)
  - [Video processing scheme](#video-processing-scheme)
- [Running with Docker](#running-with-docker)
  - [env](#env)
  - [Launching](#launching)

---

# Structure

The project includes two microservices and React-based frontend.

## General structure
```mermaid
stateDiagram
  direction TB
  front --> back:Video URL
  back --> front:Result with summary
  back --> postgres
  back --> redis:Add task to queue
  back --> cache
  cache --> back
  redis --> back:Get result
  postgres --> back
  proc --> redis:Set result
  redis --> proc:Get task
  front:React Frontend
  back:Go backend
  postgres:PostgreSQL
  redis:Redis
  proc:Video Processor
  cache: Redis (Caching) 
```

## Services interaction

```mermaid
sequenceDiagram
  participant front as Frontend
  participant back as Backend
  participant redis as Redis (queue)
  participant proc as Video Processor

  front->>+back: Video URL
  back->>+redis: Video URL
  redis-->>+proc: Get task from queue
  Note over redis: Task in queue
  Note over proc: Processing task
  proc-->>-redis: Set result data 
  redis-->>back: Result data
  back-->>-front: Result data with summary
```

## Video processing scheme
```mermaid
sequenceDiagram
  participant redis as Redis
  participant tube as YouTube <br> processor
  participant transcr as Transcriber <br> (OpenAI Whisper)
  participant splitter as Text Splitter
  participant corrector as Spell Corrector <br> (ruT5)
  participant summ as Summarizer <br> (ruT5)
  
  redis->>+tube: Video URL
  Note over tube: Save video metadata
  tube->>-transcr: Audio data
  activate transcr
  transcr->>-splitter: Transcribed text <br> with timestamps
  splitter->>corrector: Splitted text <br> by chunks
  loop
    corrector->>+summ: Summarize chunk
    Note over summ: Concatenate <br> results
    summ-->>-corrector: 
  end
  summ->>redis: Result with timestamps and metadata
```



# Running with Docker

## env

All modules include example.env files. You should create `.env` files with these examples and put them in the same directory.
Global `.env` file in the root directory must include:
```bash
REDIS_PASSWORD="<password>"

POSTGRES_USERNAME="<username>"
POSTGRES_PASSWORD="<password>"
POSTGRES_DATABASE="<database_name>"
```
**these variables must be identical in all `.env` files.**

## Launching

**Note: Docker and Docker Compose are required for launch.**
To build and launch the entire project:
```shell
docker compose up -d --build
```

Launching without building:
```shell
docker compose up -d
```

*Recommended first launch without `-d` flag to troubleshoot errors and verify configuration correctness.* 

To stop all containers:
```shell
docker compose down
```

To stop with deleting volumes with saved data:
```shell
docker compose down -v
```

*In your system the command may be `docker-compose` instead of `docker compose`*.

After launching the frontend will be available on `http://localhost:80`