from fastapi import APIRouter
from .service import router as _auth

router = APIRouter()
router.include_router(_auth)