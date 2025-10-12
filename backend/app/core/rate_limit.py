from fastapi import Request, HTTPException
import redis.asyncio as redis
from .config import get_settings

_settings = get_settings()
_redis = redis.from_url(_settings.REDIS_URL)

def RateLimit(max_req: int = 200, per_seconds: int = 60):
    async def middleware(request: Request, call_next):
        ip = (request.client.host if request.client else "unknown")
        key = f"ratelimit:{ip}"
        async with _redis.pipeline() as pipe:
            await pipe.incr(key, 1)
            await pipe.expire(key, per_seconds)
            count, _ = await pipe.execute()
        if int(count) > max_req:
            raise HTTPException(status_code=429, detail="Too many requests")
        return await call_next(request)
    return middleware