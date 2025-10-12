import os
from functools import lru_cache

class Settings:
    ENV = os.getenv("ENV","dev")
    DOMAIN = os.getenv("DOMAIN","localhost")
    DB_URL = os.getenv("DB_URL","sqlite:///./app.db")
    REDIS_URL = os.getenv("REDIS_URL","redis://localhost:6379/0")
    JWT_SECRET = os.getenv("JWT_SECRET","change-me")
    ACCESS_TTL_MIN = int(os.getenv("ACCESS_TTL_MIN","30"))
    REFRESH_TTL_DAYS = int(os.getenv("REFRESH_TTL_DAYS","7"))
    PASSWORD_MIN_LEN = int(os.getenv("PASSWORD_MIN_LEN","10"))
    SMTP_HOST = os.getenv("SMTP_HOST","localhost")
    SMTP_PORT = int(os.getenv("SMTP_PORT","1025"))
    SMTP_FROM = os.getenv("SMTP_FROM","noreply@localhost")
    TOTP_ISSUER = os.getenv("TOTP_ISSUER","HeartLink")
    S3_ENDPOINT = os.getenv("S3_ENDPOINT")
    S3_REGION = os.getenv("S3_REGION","us-east-1")
    S3_BUCKET = os.getenv("S3_BUCKET")
    S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
    S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
    S3_USE_PATH_STYLE = os.getenv("S3_USE_PATH_STYLE","0") == "1"
    MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB","15"))
    CLAMAV_HOST = os.getenv("CLAMAV_HOST","clamav")
    CLAMAV_PORT = int(os.getenv("CLAMAV_PORT","3310"))
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
    STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
    CORS_ORIGINS = [s.strip() for s in os.getenv("CORS_ORIGINS","http://localhost:3000").split(",")]
    LOG_LEVEL = os.getenv("LOG_LEVEL","INFO")

@lru_cache
def get_settings():
    return Settings()
