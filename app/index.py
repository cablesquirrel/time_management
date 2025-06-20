"""API router for Index."""

from api.v1.index import router as api_v1_router
from fastapi import APIRouter

router: APIRouter = APIRouter()
router.prefix = "/api"
router.include_router(
    api_v1_router,
    prefix="/v1",
    tags=None,
)
