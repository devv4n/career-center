FROM golang:1.23-alpine AS builder

RUN apk update && apk add --no-cache git make

WORKDIR /app

COPY go.mod go.sum ./

RUN go mod download

COPY . .

RUN make build

FROM alpine:latest

WORKDIR /app

USER nobody
CMD ["./career-center"]
