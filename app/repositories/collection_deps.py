from typing import Callable
from motor.motor_asyncio import AsyncIOMotorCollection
from src.core.database import mongodb


def get_db_collection(name: str) -> Callable[[], AsyncIOMotorCollection]:
    """Returns a dependency that provides a collection."""
    def dependency() -> AsyncIOMotorCollection:
        return mongodb.db[name]
    return dependency
