"""
Test configuration for gomoku backend tests
"""
import os
from typing import Optional


class TestConfig:
    """Configuration class for test environment"""
    
    # Test database settings
    TEST_MONGO_URL = "mongodb://localhost:27017"
    TEST_MONGO_DB_NAME = "gomoku_test"
    
    # Test authentication settings  
    TEST_SECRET_KEY = "test_secret_key_for_jwt_tokens_in_testing_environment_only"
    TEST_ALGORITHM = "HS256"
    TEST_ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    @classmethod
    def get_test_db_url(cls) -> str:
        """Get test database URL"""
        return os.getenv("TEST_MONGO_URL", cls.TEST_MONGO_URL)
    
    @classmethod  
    def get_test_db_name(cls) -> str:
        """Get test database name"""
        return os.getenv("TEST_MONGO_DB_NAME", cls.TEST_MONGO_DB_NAME)
    
    @classmethod
    def setup_test_environment(cls):
        """Setup environment variables for testing"""
        os.environ["TEST_MONGO_URL"] = cls.get_test_db_url()
        os.environ["TEST_MONGO_DB_NAME"] = cls.get_test_db_name()
        os.environ["ACCESS_TOKEN_SECRET_KEY"] = cls.TEST_SECRET_KEY
        os.environ["ALGORITHM"] = cls.TEST_ALGORITHM
