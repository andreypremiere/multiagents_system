from fastapi import APIRouter

from backend.app.api.v1.endpoints import auth, users

router = APIRouter()

router.include_router(auth.router)
router.include_router(users.router)


@router.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "personal-ai-workstation",
    }
