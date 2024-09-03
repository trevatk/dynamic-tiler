
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from titiler.core.factory import TilerFactory
from titiler.extensions import wmsExtension
from titiler.core.errors import DEFAULT_STATUS_CODES, add_exception_handlers

from src.dependencies import DatasetPathParams

app = FastAPI()

protected_router = TilerFactory(path_dependency=DatasetPathParams, extensions=[
    wmsExtension()
])

unprotected_router = TilerFactory(extensions=[
    wmsExtension()
])

app.include_router(protected_router.router, prefix='/protected')
app.include_router(unprotected_router.router)

add_exception_handlers(app, DEFAULT_STATUS_CODES)

@app.get("/health", description="Health Check", tags=["Health Check"])
def ping():
    return {"ping": "pong"}
