
from pydantic_settings import BaseSettings

class AuthSettings(BaseSettings):

    username: str = 'test'
    password: str = 'test123'

    class Config:
        env_prefix = "SECURITY_"

auth_config = AuthSettings()