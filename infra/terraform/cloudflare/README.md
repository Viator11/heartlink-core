# Cloudflare Terraform (heartlink.love)

## Переменные
- `cloudflare_api_token` — токен с доступом к DNS и (опционально) R2/Images.
- `cloudflare_account_id` — ID аккаунта в Cloudflare.
- `zone` — `heartlink.love`
- `r2_bucket_name` — имя бакета, по умолчанию `heartlink-media`

## DNS
Файл создаёт записи:
- app.heartlink.love
- api.heartlink.love
- stage.heartlink.love
- cdn.heartlink.love
- mail.heartlink.love

Значения CNAME сейчас-заглушки: `your.*.host` — замените на ваш публичный хост (VPS/Load Balancer).
