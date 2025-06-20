"""API routers for Index."""

from api.v1.remote import router as remote_router
from fastapi import APIRouter

router = APIRouter()

router.include_router(
    remote_router.router,
    prefix="/remote",
    tags=["Remote Control Device"],
)
