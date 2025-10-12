from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, generate_latest
from starlette.responses import Response
from .core.config import get_settings
from .auth.router import router as auth_router
from .profiles.router import router as profiles_router
from .matches.router import router as matches_router
from .chat.websocket import manager as ws_manager
from .gdpr.router import router as gdpr_router
from .billing.stripe_api import router as billing_router
from .moderation.ai import moderate_text
import structlog, time

settings = get_settings()
app = FastAPI(title="HeartLink v3.0 Pro", version="3.0")

# Logging
log = structlog.get_logger()

# Metrics
REQ_COUNTER = Counter("http_requests_total", "Total HTTP requests")

@app.middleware("http")
async def metrics_middleware(request, call_next):
    start = time.time()
    response = await call_next(request)
    REQ_COUNTER.inc()
    log.info("request", path=request.url.path, status=response.status_code, dur=round(time.time()-start,3))
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/metrics")
def metrics(): return Response(generate_latest(), media_type="text/plain")

@app.get("/moderate-test")
def modtest(text:str):
    return {"ok": moderate_text(text)}

# Routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(profiles_router, prefix="/profiles", tags=["profiles"])
app.include_router(matches_router, prefix="/matches", tags=["matches"])
app.include_router(gdpr_router, prefix="/gdpr", tags=["gdpr"])
app.include_router(billing_router, prefix="/billing", tags=["billing"])

# WebSocket chat
@app.websocket("/ws/{user_id}")
async def chat_ws(ws: WebSocket, user_id: int):
    await ws_manager.connect(user_id, ws)
    try:
        while True:
            data = await ws.receive_text()
            await ws_manager.broadcast(user_id, data)
    except WebSocketDisconnect:
        ws_manager.disconnect(user_id)