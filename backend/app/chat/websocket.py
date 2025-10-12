from typing import Dict, List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from ..core.security import verify_token

router = APIRouter(prefix="/ws", tags=["chat"])

class Manager:
    def __init__(self):
        self.rooms: Dict[str, List[WebSocket]] = {}

    async def connect(self, room: str, ws: WebSocket):
        await ws.accept()
        self.rooms.setdefault(room, []).append(ws)

    def remove(self, room: str, ws: WebSocket):
        if room in self.rooms and ws in self.rooms[room]:
            self.rooms[room].remove(ws)

    async def broadcast(self, room: str, msg: dict):
        for ws in list(self.rooms.get(room, [])):
            try:
                await ws.send_json(msg)
            except Exception:
                self.remove(room, ws)

manager = Manager()

@router.websocket("/chat")
async def chat_ws_endpoint(websocket: WebSocket, token: str = Query(...), room: str = Query(...)):
    data = verify_token(token)
    uid = int(data["sub"])
    await manager.connect(room, websocket)
    try:
        while True:
            payload = await websocket.receive_json()
            payload["sender_id"] = uid
            await manager.broadcast(room, payload)
    except WebSocketDisconnect:
        manager.remove(room, websocket)