import logging
import time

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

load_dotenv()

class Config(BaseSettings):
    MONGO_DB_URI:str
    AUTH_JWT_SECRET_KEY:str
    OLLAMA_API_URL: str = "http://localhost:11434/api/chat"
    OLLAMA_MODEL: str = "gemma3:4b"
    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET_NAME: str = "images"

    model_config = SettingsConfigDict(env_file="../../.env", extra="ignore")

config = Config()

logger = logging.getLogger("uvicorn")


def register_middleware(app: FastAPI):
    """
    Register middleware for logging and token validation.
    :param app: FastAPI instance
    :return: None
    """

    @app.middleware("http")
    async def custom_logging(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        processing_time = time.time() - start_time
        message = (
            f"{request.client.host}:{request.client.port} - {request.method} "
            f"- {request.url.path} - {response.status_code} completed after {processing_time:.2f}s"
        )
        print(message)

        return response


    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )