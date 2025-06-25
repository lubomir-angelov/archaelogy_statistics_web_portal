# app/config.py
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    DEBUG: bool
    TESTING: bool 
    CSRF_ENABLED: bool
    SECRET_KEY: str
    # e.g. postgres://user:pass@host/db
    DATABASE_URL: str 


def create_test_settings() -> Settings:
    return Settings(
        DEBUG = True,
        TESTING = True,
        CSRF_ENABLED = False,
        SECRET_KEY= 'test',
        DATABASE_URL = 'sqlite:///./test.db'
    )

def create_settings() -> Settings:
    return Settings(
        DEBUG = False,
        TESTING = False,
        CSRF_ENABLED = True,
        SECRET_KEY = os.getenv('SECRET_KEY'),
        DATABASE_URL = os.getenv('DATABASE_URL')
    )
