# CHANGELOG — HL-1 (Prod Deploy Bootstrap)
Date: 2025-10-12 09:14 UTC

- Добавлены Terraform-скелеты для Cloudflare (зона, DNS записи app/api/stage/cdn/mail).
- Добавлен Terraform-скелет для Hetzner Managed Postgres.
- Добавлены .env.example для backend и frontend.
- Улучшен docker-compose: healthchecks.
- Добавлен Makefile с целями up-local / terraform.
- Обновлена документация (README/CF README).
