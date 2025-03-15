from fastapi import APIRouter

from app_fastapi.routers.root.urls import Prefixes, Endpoints

from . import http_methods

router = APIRouter(prefix=Prefixes.HEALTH_CHECK)

router.get(Endpoints.ENDPOINT)(http_methods.http_get)
