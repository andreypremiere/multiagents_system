from fastapi import APIRouter

from backend.app.api.v1.endpoints import (
    auth,
    chats,
    options,
    projects,
    provider_credentials,
    users,
)

router = APIRouter()

router.include_router(auth.router)
router.include_router(users.router)
router.include_router(projects.router)
router.include_router(chats.router)
router.include_router(provider_credentials.router)
router.include_router(options.router)


@router.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "personal-ai-workstation",
    }
