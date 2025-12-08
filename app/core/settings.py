from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "Coaching Company AI System"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # OpenAI
    OPENAI_API_KEY: str
    
    # Environment
    ENVIRONMENT: str = "local"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
