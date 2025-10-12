from typing import Optional
from fastapi import APIRouter, Header, HTTPException, Depends
from sqlmodel import Session, select
from ..core.security import verify_token
from ..db.session import get_session
from ..models.profile import Profile
from ..models.match import Match

router = APIRouter(prefix="/matches", tags=["matches"])

def _uid(auth: Optional[str]) -> int:
    if not auth or not auth.lower().startswith("bearer "): raise HTTPException(401, "Unauthorized")
    return int(verify_token(auth.split()[1])["sub"])

@router.get("/discover")
def discover(authorization: Optional[str] = Header(None), session: Session = Depends(get_session)):
    uid = _uid(authorization)
    return session.exec(select(Profile).where(Profile.user_id != uid).limit(50)).all()

@router.post("/pair/{other_id}")
def pair(other_id: int, authorization: Optional[str] = Header(None), session: Session = Depends(get_session)):
    uid = _uid(authorization)
    existing = session.exec(select(Match).where(
        (Match.user1_id == uid) & (Match.user2_id == other_id)
    )).first()
    if existing: return existing
    m = Match(user1_id=uid, user2_id=other_id)
    session.add(m); session.commit(); session.refresh(m)
    return m