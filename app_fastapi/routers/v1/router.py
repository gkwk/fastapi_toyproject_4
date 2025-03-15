from fastapi import APIRouter

from app_fastapi.routers.v1.urls import Prefixes

from .users import router as users_router

router = APIRouter(prefix=Prefixes.API_ROUTER)

router.include_router(users_router.router)
