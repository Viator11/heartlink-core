import time
from typing import Callable, Awaitable
from fastapi import Request
from starlette.responses import JSONResponse

WINDOWS = {}

def limiter(max_requests: int, window_seconds: int, scope: str):
    def decorator(handler: Callable[..., Awaitable]):
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request") or args[0]
            ip = request.headers.get("CF-Connecting-IP") or request.client.host
            key = f"{scope}:{ip}"
            now = int(time.time())
            win = WINDOWS.get(key, {"from": now, "count": 0})
            if now - win["from"] >= window_seconds:
                win = {"from": now, "count": 0}
            win["count"] += 1
            WINDOWS[key] = win
            if win["count"] > max_requests:
                retry_after = max(1, window_seconds - (now - win["from"]))
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": "rate_limited",
                        "details": "Too many requests",
                        "retry_after": retry_after,
                        "limit_scope": scope,
                    },
                    headers={"Retry-After": str(retry_after)},
                )
            return await handler(*args, **kwargs)
        return wrapper
    return decorator
