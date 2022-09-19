from distutils.debug import DEBUG
from pydantic import BaseSettings
from functools import lru_cache



class Settings(BaseSettings):
    debug: bool = False
    echo_active: bool = True
    
    class Config:
        env_file = '.env'


@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
DEBUG = settings.debug