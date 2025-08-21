"""
Pytest configuration and fixtures for backend tests
"""
import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient
from backend.main import app
from backend.core.database import MongoAsyncClient
from backend.tests.test_config import TestConfig


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)  
async def setup_test_environment():
    """Setup test environment variables"""
    TestConfig.setup_test_environment()
    yield


@pytest.fixture(scope="function")
async def test_db() -> AsyncGenerator[MongoAsyncClient, None]:
    """
    Create a test database client and clean up after each test
    """
    # Create test database client
    db_client = MongoAsyncClient(
        test_mode=True,
        test_db_url=TestConfig.get_test_db_url(), 
        test_db_name=TestConfig.get_test_db_name()
    )
    
    yield db_client
    
    # Cleanup: Drop all collections after each test
    collections = await db_client.db.list_collection_names()
    for collection_name in collections:
        await db_client.db[collection_name].drop()
    
    # Close database connection
    await db_client.close()


@pytest.fixture(scope="function") 
async def client(test_db) -> AsyncGenerator[AsyncClient, None]:
    """
    Create test HTTP client for API testing
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def test_user_data():
    """Test user data for creating users in tests"""
    return [
        {
            "email": "test.user1@example.com",
            "name": "Test User 1", 
            "pwd": "testpassword123"
        },
        {
            "email": "test.user2@example.com", 
            "name": "Test User 2",
            "pwd": "testpassword456"
        }
    ]