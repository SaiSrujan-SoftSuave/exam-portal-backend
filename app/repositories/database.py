import json
import os
import certifi
import pydantic
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure

from app.core.config import config, logger


class DataBase:
    """
      Manages the connection to MongoDB and provides a database instance.
      This class follows the singleton pattern to ensure only one client is created.
      """
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None


mongodb = DataBase()

async def connect_to_mongo():
    """
           Establishes the connection to the MongoDB server.
           """
    try:
        print("mongo uri",config.MONGO_DB_URI)
        mongodb.client = AsyncIOMotorClient(
            config.MONGO_DB_URI,
            tlsCAFile=certifi.where(),
            uuidRepresentation="standard",
            retryWrites=True,
            retryReads=True
        )
        await mongodb.client.admin.command("ping")
        mongodb.db = mongodb.client["exam_portal_db"]
        print("Connected to MongoDB")

    except ServerSelectionTimeoutError as e:
        logger.error(f"Server selection timeout: {e}")
        raise
    except ConnectionFailure as e:
        logger.error(f"Connection failure: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected MongoDB error: {e}")
        raise

async def close_mongo_connection():
    """
          Closes the active MongoDB connection.
          """
    try:
        if mongodb.client:
            mongodb.client.close()
            logger.info("MongoDB connection closed")
    except Exception as e:
        logger.error(f"Error closing MongoDB connection: {e}")


def get_db() -> AsyncIOMotorDatabase:
    if mongodb.db is None:
        raise RuntimeError("Database not initialized. Call connect_to_mongo() first.")
    return mongodb.db