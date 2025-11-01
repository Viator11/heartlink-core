# APPLY_HL2_FULL.md — быстрый запуск
1) GitHub Secrets: CF_API_TOKEN, CF_ACCOUNT_ID, HCLOUD_TOKEN, POSTMARK_API_TOKEN, SMTP_FROM=noreply@mail.heartlink.love
2) Postmark: импортируйте postmark/postmark_template_verify.json (alias: verify-email).
3) Alembic: добавьте ревизии user_sessions и security_logs, примените миграции.
4) Деплой stage: make tf-init && make tf-plan && make tf-apply (после добавления реальных ресурсов).
5) Проверка: /auth/register -> письмо -> /auth/verify; /auth/devices; /auth/device/logout-all.
