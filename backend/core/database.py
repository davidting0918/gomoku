from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv("backend/.env")

class MongoAsyncClient:
    def __init__(self):
        self.db_url = os.getenv("MONGO_URL")
        self.db_name = os.getenv("MONGO_DB_NAME")
        self.client = AsyncIOMotorClient(self.db_url)
        self.db = self.client[self.db_name]

    def list_collections(self):
        """List all collections in the database"""
        return self.db.list_collection_names()

    async def insert_one(self, collection: str, document: dict):
        """Create a single document"""
        collection = self.db[collection]
        result = await collection.insert_one(document)
        return result.inserted_id

    async def insert_many(self, collection: str, documents: list[dict]):
        """Create multiple documents"""
        collection = self.db[collection]
        result = await collection.insert_many(documents)
        return result.inserted_ids

    async def find_one(self, collection: str, filter: dict):
        """Find a single document"""
        collection = self.db[collection]
        return await collection.find_one(filter)

    async def find_many(self, collection: str, filter: dict = None):
        """Find multiple documents"""
        collection = self.db[collection]
        if filter is None:
            filter = {}
        cursor = collection.find(filter)
        return await cursor.to_list(length=None)

    async def update_one(self, collection: str, filter: dict, update: dict):
        """Update a single document"""
        collection = self.db[collection]
        result = await collection.update_one(filter, {"$set": update})
        return result.modified_count

    async def update_many(self, collection: str, filter: dict, update: dict):
        """Update multiple documents"""
        collection = self.db[collection]
        result = await collection.update_many(filter, {"$set": update})
        return result.modified_count

    async def delete_one(self, collection: str, filter: dict):
        """Delete a single document"""
        collection = self.db[collection]
        result = await collection.delete_one(filter)
        return result.deleted_count

    async def delete_many(self, collection: str, filter: dict):
        """Delete multiple documents"""
        collection = self.db[collection]
        result = await collection.delete_many(filter)
        return result.deleted_count

    async def close(self):
        """Close the database connection"""
        self.client.close()
        
        