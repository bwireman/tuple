FROM golang:1.13

WORKDIR /app
COPY ./pilot . 
RUN go get ./...
RUN go build -o pilot ./cmd/main.go
RUN pwd
RUN ls

ENTRYPOINT [ "./pilot" ]