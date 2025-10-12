from fastapi import APIRouter, Header, HTTPException, Depends
from sqlmodel import Session, select
from ..core.security import verify_token
from ..db.session import get_session
from ..models.user import User
from ..models.profile import Profile
from ..models.message import Message
from ..models.match import Match

router = APIRouter(prefix="/gdpr", tags=["gdpr"])

def _uid(auth: str) -> int:
    if not auth.lower().startswith("bearer "): raise HTTPException(401, "Unauthorized")
    return int(verify_token(auth.split()[1])["sub"])

@router.get("/export")
def export(authorization: str = Header(...), session: Session = Depends(get_session)):
    uid = _uid(authorization)
    user = session.get(User, uid)
    prof = session.exec(select(Profile).where(Profile.user_id==uid)).first()
    matches = session.exec(select(Match).where((Match.user1_id==uid) | (Match.user2_id==uid))).all()
    messages = session.exec(select(Message).where(Message.sender_id==uid)).all()
    return {
        "user": user.model_dump() if user else None,
        "profile": prof.model_dump() if prof else None,
        "matches": [m.model_dump() for m in matches],
        "messages": [m.model_dump() for m in messages],
    }

@router.delete("/delete")
def delete(authorization: str = Header(...), session: Session = Depends(get_session)):
    uid = _uid(authorization)
    user = session.get(User, uid)
    if not user: return {"ok": True}
    session.delete(user); session.commit()
    return {"ok": True}