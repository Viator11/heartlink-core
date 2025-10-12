# HeartLink Backend (fixed)

## Local run with Docker
```bash
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000  # if running without Docker
```

With docker-compose (from project infra):
```bash
docker compose up --build
```

## Alembic
```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```
