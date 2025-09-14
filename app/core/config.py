import logging

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Config(BaseSettings):
    MONGO_DB_URI:str
    AUTH_JWT_SECRET_KEY:str
    OLLAMA_API_URL: str = "http://localhost:11434/api/chat"
    OLLAMA_MODEL: str = "gemma3:4b"

    model_config = SettingsConfigDict(env_file="../../.env", extra="ignore")

config = Config()

logger = logging.getLogger("uvicorn")