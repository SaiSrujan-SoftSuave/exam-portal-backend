import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URI = os.getenv("MONOGO_DB_URI")

client = AsyncIOMotorClient(MONGO_DB_URI)
database = client.get_database("exam_portal")
