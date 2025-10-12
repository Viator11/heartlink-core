
# heartlink-core

Monorepo для HeartLink (домен: `heartlink.love`). Стек: FastAPI (backend), Next.js (frontend), Docker, Terraform (Cloudflare + Hetzner), GitHub Actions CI/CD.

Сгенерировано: 2025-10-12 08:47 UTC

## Структура
- `backend/` — FastAPI + Alembic + Stripe webhooks + Geo
- `frontend/` — Next.js + Tailwind + i18n scaffold
- `infra/`
  - `docker/` — compose для local/stage/prod
  - `terraform/cloudflare` — зона, DNS, R2, Images, worker routes
  - `terraform/hetzner` — Managed Postgres
  - `github-ci/` — GitHub Actions
  - `caddy/` — Caddyfile (reverse proxy для app/api)

## Домены
- app.heartlink.love — фронтенд
- api.heartlink.love — бэкенд
- stage.heartlink.love — стейдж
- cdn.heartlink.love — CDN для медиа
- mail.heartlink.love — письма

## Быстрый старт (локально)
```bash
# запуск локально (без секретов продакшена)
cd infra/docker
docker compose -f docker-compose.local.yml up -d --build
```

## Деплой
CI/CD настроен на ветки:
- `staging` → деплой на stage
- `main` → деплой на prod

Секреты через GitHub OIDC (Cloudflare/Hetzner), без хранения .env в репо.
