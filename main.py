
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from titiler.core.factory import TilerFactory
from titiler.extensions import wmsExtension
from titiler.core.errors import DEFAULT_STATUS_CODES, add_exception_handlers

from src.dependencies import DatasetPathParams
from src.extensions import wmsExtension as authenticatedWmsExtension
from src.routes import router

app = FastAPI()

origins = [
    "http://*",
    "https://*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

protected_router = TilerFactory(path_dependency=DatasetPathParams, extensions=[
    authenticatedWmsExtension()
])

unprotected_router = TilerFactory(extensions=[
    wmsExtension()
])

app.include_router(protected_router.router, prefix='/protected')
app.include_router(unprotected_router.router)
app.include_router(router)

add_exception_handlers(app, DEFAULT_STATUS_CODES)

@app.get("/health", description="Health Check", tags=["Health Check"])
def ping():
    return {"ping": "pong"}

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=4000)
