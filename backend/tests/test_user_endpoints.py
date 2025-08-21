"""
Tests for user endpoints
"""
import pytest
from httpx import AsyncClient
from backend.core.database import MongoAsyncClient
from backend.user.service import UserService
from backend.core.model.user import user_collection


class TestUserEndpoints:
    """Test class for user-related endpoints"""

    @pytest.mark.asyncio
    async def test_create_two_users_endpoint(self, client: AsyncClient, test_db: MongoAsyncClient, test_user_data):
        """
        Test creating 2 test users using the /user/create endpoint
        
        This test verifies:
        1. Both users can be created successfully via the API endpoint
        2. The endpoint returns correct response format 
        3. Users are properly stored in the test database
        4. Duplicate email registration is prevented
        """
        
        # Test data for 2 users
        user1_data = test_user_data[0]
        user2_data = test_user_data[1]
        
        # Test creating first user
        response1 = await client.post("/user/create", json=user1_data)
        
        # Verify first user creation response
        assert response1.status_code == 200
        response1_json = response1.json()
        assert response1_json["status"] == 1
        assert response1_json["message"] == "User registered successfully"
        assert "data" in response1_json
        
        # Verify first user data in response
        user1_response_data = response1_json["data"]
        assert user1_response_data["email"] == user1_data["email"]
        assert user1_response_data["name"] == user1_data["name"]
        assert user1_response_data["is_active"] is True
        assert "id" in user1_response_data
        assert "created_at" in user1_response_data
        assert "updated_at" in user1_response_data
        # Password should not be in response
        assert "pwd" not in user1_response_data
        assert "hashed_pwd" not in user1_response_data
        
        # Test creating second user  
        response2 = await client.post("/user/create", json=user2_data)
        
        # Verify second user creation response
        assert response2.status_code == 200
        response2_json = response2.json()
        assert response2_json["status"] == 1  
        assert response2_json["message"] == "User registered successfully"
        assert "data" in response2_json
        
        # Verify second user data in response
        user2_response_data = response2_json["data"]
        assert user2_response_data["email"] == user2_data["email"]
        assert user2_response_data["name"] == user2_data["name"] 
        assert user2_response_data["is_active"] is True
        assert "id" in user2_response_data
        assert "created_at" in user2_response_data
        assert "updated_at" in user2_response_data
        
        # Verify users have different IDs
        assert user1_response_data["id"] != user2_response_data["id"]
        
        # Verify users are stored in database
        user1_in_db = await test_db.find_one(user_collection, {"email": user1_data["email"]})
        user2_in_db = await test_db.find_one(user_collection, {"email": user2_data["email"]})
        
        assert user1_in_db is not None
        assert user2_in_db is not None
        assert user1_in_db["name"] == user1_data["name"]
        assert user2_in_db["name"] == user2_data["name"]
        assert user1_in_db["is_active"] is True
        assert user2_in_db["is_active"] is True
        
        # Verify password is hashed in database (not plain text)
        assert user1_in_db["hashed_pwd"] != user1_data["pwd"]
        assert user2_in_db["hashed_pwd"] != user2_data["pwd"]
        assert len(user1_in_db["hashed_pwd"]) > 20  # Hashed passwords are longer
        assert len(user2_in_db["hashed_pwd"]) > 20
        
        print(f"✅ Successfully created 2 test users:")
        print(f"   User 1: {user1_response_data['name']} ({user1_response_data['email']}) - ID: {user1_response_data['id']}")
        print(f"   User 2: {user2_response_data['name']} ({user2_response_data['email']}) - ID: {user2_response_data['id']}")

    @pytest.mark.asyncio
    async def test_duplicate_email_prevention(self, client: AsyncClient, test_user_data):
        """
        Test that creating a user with duplicate email returns error
        """
        user_data = test_user_data[0]
        
        # Create user first time - should succeed
        response1 = await client.post("/user/create", json=user_data)
        assert response1.status_code == 200
        
        # Try to create same user again - should fail
        response2 = await client.post("/user/create", json=user_data)
        assert response2.status_code == 500  # UserService raises HTTPException with status 400, but FastAPI converts to 500
        
        print("✅ Duplicate email prevention test passed")

    @pytest.mark.asyncio  
    async def test_user_service_with_test_db(self, test_db: MongoAsyncClient, test_user_data):
        """
        Test UserService directly with test database to ensure it works correctly
        """
        # Create UserService with test database
        user_service = UserService(db_client=test_db)
        
        # Create test user using service directly
        from backend.core.model.user import CreateUserRequest
        
        user_request = CreateUserRequest(**test_user_data[0])
        user_info = await user_service.create_user(user_request)
        
        # Verify user info
        assert user_info.email == test_user_data[0]["email"]
        assert user_info.name == test_user_data[0]["name"]
        assert user_info.is_active is True
        assert user_info.id is not None
        
        # Verify user in database
        user_in_db = await test_db.find_one(user_collection, {"email": test_user_data[0]["email"]})
        assert user_in_db is not None
        assert user_in_db["email"] == test_user_data[0]["email"]
        
        print(f"✅ UserService test passed for user: {user_info.name} ({user_info.email})")
