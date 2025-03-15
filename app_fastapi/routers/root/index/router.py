from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app_fastapi.routers.root.urls import Prefixes, Endpoints

from . import http_methods

router = APIRouter(prefix=Prefixes.INDEX)

router.get(Endpoints.ENDPOINT_SLASH, response_class=HTMLResponse)(http_methods.http_get)
