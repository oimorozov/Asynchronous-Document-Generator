# Asynchronous-Document-Generator

Проект не расчитан на решение каких-либо задач, тем более иновационных, лишь тестирование технического стэка технологий

MVP для асинхронной загрузки и получения файлов: фронт, gateway, worker, MinIO, RabbitMQ, Postgres.

## Архитектура
- Frontend (Nginx) → Gateway (FastAPI) → RabbitMQ → Worker (FastAPI)
- Хранилище: MinIO
- БД: Postgres

## Возможности
- Загрузка файла
- Получение статуса
- Скачивание результата по публичной ссылке

## Запуск
```bash
docker compose up --build
```
Открыть: `http://localhost:3000`

## API
- `POST /api/v1/upload` (multipart/form-data, `file`)
- `GET /api/v1/status/{id}`

## Переменные окружения (gateway)
- `DATABASE_URL`
- `RABBITMQ_URL`
- `MINIO_ENDPOINT`
- `MINIO_PUBLIC_ENDPOINT`
- `MINIO_ACCESS_KEY`
- `MINIO_SECRET_KEY`

## Примечания
- Ссылка на скачивание формируется с `MINIO_PUBLIC_ENDPOINT`
- Worker в MVP копирует файл в выходной бакет

