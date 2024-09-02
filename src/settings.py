
from pydantic_settings import BaseSettings

class AuthSettings(BaseSettings):

    username: str = ""
    password: str = ""

    class Config:
        env_prefix = "SECURITY_"

auth_config = AuthSettings()