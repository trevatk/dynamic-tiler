
from typing import Annotated

from fastapi import HTTPException, Query, Security, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

def DatasetPathParams(
    url: str = Query(..., description="Dataset URL"),
    credentials = Security(security)
):
    if credentials.username is None or credentials.password is None:
        raise HTTPException(status_code=403, detail='no credentials provided')
    
    return url