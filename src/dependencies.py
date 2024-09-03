
from typing import Annotated

from fastapi import HTTPException, Query, Security, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.models import BasicAuth

security = HTTPBasic()

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    if not BasicAuth.validate_basic_credentials(credentials):
        raise HTTPException(status_code=401)
    return credentials.username

def DatasetPathParams(
    url: str = Query(..., description="Dataset URL"),
    credentials = Security(security),
    current_user: str = Depends(get_current_user)
):
    return url