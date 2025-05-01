FROM golang:1.24.2-alpine AS builder

RUN apk add --no-cache git
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /app/bin/app /app/cmd/server/main.go

# ------------------------------------ #
FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /app

COPY .env /app/.env
COPY --from=builder /app/bin/app /app/app

EXPOSE 8000

CMD ["/app/app"]