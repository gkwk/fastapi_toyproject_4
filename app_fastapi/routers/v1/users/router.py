from fastapi import APIRouter

from app_fastapi.routers.v1.urls import Prefixes, Endpoints
from app_fastapi.routers.v1.tags import Tags

from . import http_methods

router = APIRouter(prefix=Prefixes.USERS_ROUTER, tags=[Tags.USER])

router.get(Endpoints.ENDPOINT)(http_methods.http_get)
router.post(Endpoints.ENDPOINT)(http_methods.http_post)
router.patch(Endpoints.ENDPOINT)(http_methods.http_patch)
router.delete(Endpoints.ENDPOINT)(http_methods.http_delete)
