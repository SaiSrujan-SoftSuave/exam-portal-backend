from typing import Callable
from motor.motor_asyncio import AsyncIOMotorCollection
from app.repositories.database import mongodb


def get_db_collection(name: str) -> Callable[[], AsyncIOMotorCollection]:
    """Returns a dependency that provides a collection."""
    def dependency() -> AsyncIOMotorCollection:
        return mongodb.db[name]
    return dependency

get_questions_collection = get_db_collection("questions")
get_results_collection = get_db_collection("results")