import logging
from logging import Logger

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    MONGO_DB_URI:str

config = Config()
logger = logging.getLogger("uvicorn")