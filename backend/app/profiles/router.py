from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, Header, HTTPException
from sqlmodel import Session, select
from ..db.session import get_session
from ..models.profile import Profile
from ..core.security import verify_token
from ..core.config import get_settings
from ..utils.antivirus import scan_bytes
from ..utils.thumbnails import make_thumbnail
from ..utils.storage import put_object, get_presigned_url
import json, secrets

router = APIRouter(prefix="/profiles", tags=["profiles"])
s = get_settings()

def _uid(authorization: Optional[str]) -> int:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(401, "Unauthorized")
    data = verify_token(authorization.split()[1])
    return int(data["sub"])

@router.get("/me")
def me(authorization: Optional[str] = Header(None), session: Session = Depends(get_session)):
    uid = _uid(authorization)
    prof = session.exec(select(Profile).where(Profile.user_id == uid)).first()
    return prof

@router.post("/update")
def update(
    authorization: Optional[str] = Header(None),
    display_name: Optional[str] = Form(None),
    bio: Optional[str] = Form(None),
    interests: Optional[str] = Form(None),
    session: Session = Depends(get_session)
):
    uid = _uid(authorization)
    prof = session.exec(select(Profile).where(Profile.user_id == uid)).first() or Profile(user_id=uid)
    if display_name is not None: prof.display_name = display_name
    if bio is not None: prof.bio = bio
    if interests is not None: prof.interests = interests
    session.add(prof); session.commit(); session.refresh(prof)
    return prof

@router.post("/upload-photo")
async def upload_photo(authorization: Optional[str] = Header(None), file: UploadFile = File(...), session: Session = Depends(get_session)):
    uid = _uid(authorization)
    data = await file.read()
    if not scan_bytes(data):
        raise HTTPException(400, "Virus detected")
    thumb = make_thumbnail(data)
    key = f"users/{uid}/{secrets.token_hex(8)}.jpg"
    put_object(s.S3_BUCKET, key, thumb, "image/jpeg")
    prof = session.exec(select(Profile).where(Profile.user_id == uid)).first() or Profile(user_id=uid)
    photos = json.loads(prof.photos or "[]"); photos.append(key); prof.photos = json.dumps(photos)
    session.add(prof); session.commit(); session.refresh(prof)
    url = get_presigned_url(s.S3_BUCKET, key)
    return {"key": key, "url": url}