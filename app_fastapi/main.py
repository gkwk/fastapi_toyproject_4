from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app_fastapi.configurations.configuration import origins
from app_fastapi.core.lifespans.lifespan import app_lifespan
from app_fastapi.routers.root import router as root_router
from app_fastapi.routers.v1 import router as v1_router
from app_fastapi.routers.v2 import router as v2_router


app = FastAPI(
    title="gkwk-fastapi-toyproject-4",
    version="0.1.0",
    description="gkwk-fastapi-toyproject-4",
    lifespan=app_lifespan,
    servers=None,
    docs_url=None,
    redoc_url=None,
)

sub_app_v1 = FastAPI(
    title="gkwk-fastapi-toyproject-4-api-v1",
    version="1.0.0",
    description="v1",
    docs_url="/",
    redoc_url=None,
)
sub_app_v2 = FastAPI(
    title="gkwk-fastapi-toyproject-4-api-v2",
    version="2.0.0",
    description="v2",
    docs_url="/",
    redoc_url=None,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

app.mount("/v1", sub_app_v1)
app.mount("/v2", sub_app_v2)

app.include_router(root_router.router)
sub_app_v1.include_router(v1_router.router)
sub_app_v2.include_router(v2_router.router)
