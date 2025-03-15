import contextlib

from fastapi import FastAPI


@contextlib.asynccontextmanager
async def app_lifespan(app: FastAPI):
    print("START : lifespan")
    yield
    print("SHUTDOWN : lifespan")
