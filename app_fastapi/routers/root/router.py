from fastapi import APIRouter

from app_fastapi.routers.root.urls import Prefixes

from .index import router as index_router
from .health_check import router as health_check_router


router = APIRouter(prefix=Prefixes.ROOT_ROUTER)

router.include_router(index_router.router)
router.include_router(health_check_router.router)
