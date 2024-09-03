
from pydantic import BaseModel, field_validator

from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials

from src.settings import auth_config

class BasicAuth(BaseModel):

    username: str
    password: str

    @field_validator("username")
    def valid_username(cls, v):
        if not v:
            raise ValueError("username can not be empty")
    
    @field_validator("password")
    def valid_password(cls, v):
        if not v:
            raise ValueError("password can not be empty")
        
    class Config:
        extra = "forbid"

    @classmethod
    def validate_basic_credentials(cls, credentials: HTTPBasicCredentials):
        if credentials.username == auth_config.username and credentials.password == auth_config.password:
            return cls(username=credentials.username, password=credentials.password)
        else:
            raise HTTPException(status_code=403, detail='incorrect auth details')