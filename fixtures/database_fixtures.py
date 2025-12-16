"""
Database Fixtures

Contains database setup/teardown fixtures.
Runs before tests to create test database and seed data.

Fixtures:
- setup_test_database: Create test DB and tables (session scope, autouse)
- test_db: Get database connection (function scope)
"""

import pytest
from utils.logger import get_logger

logger = get_logger(__name__)


class TestDatabase:
    """
    Mock database class for demonstration.
    In real project, replace with actual DB client (SQLAlchemy, psycopg2, etc.)
    """
    
    def __init__(self, db_name: str):
        """Initialize database connection"""
        self.db_name = db_name
        self.tables = {}
        self.data = {}
        logger.info(f"Database initialized: {db_name}")
    
    def create_table(self, table_name: str, schema: dict):
        """Create table with schema"""
        self.tables[table_name] = schema
        self.data[table_name] = []
        logger.info(f"Table created: {table_name}")
    
    def insert(self, table_name: str, record: dict):
        """Insert record into table"""
        if table_name not in self.data:
            raise ValueError(f"Table {table_name} does not exist")
        self.data[table_name].append(record)
        logger.debug(f"Inserted into {table_name}: {record}")
    
    def query(self, table_name: str, **filters):
        """Query records from table"""
        if table_name not in self.data:
            return []
        
        results = self.data[table_name]
        
        # Filter results
        for key, value in filters.items():
            results = [r for r in results if r.get(key) == value]
        
        logger.debug(f"Query {table_name}: found {len(results)} records")
        return results
    
    def delete_all(self, table_name: str):
        """Delete all records from table"""
        if table_name in self.data:
            self.data[table_name] = []
            logger.info(f"Cleared table: {table_name}")
    
    def drop_table(self, table_name: str):
        """Drop table"""
        if table_name in self.tables:
            del self.tables[table_name]
            del self.data[table_name]
            logger.info(f"Table dropped: {table_name}")
    
    def close(self):
        """Close database connection"""
        logger.info(f"Database closed: {self.db_name}")


# Global test database instance
_test_db = None


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Setup test database before all tests (session scope, autouse).
    
    This fixture:
    - Creates mock test database
    - Creates necessary tables
    - Seeds initial test data
    - Cleans up after tests
    
    Notes:
        - autouse=True means it runs automatically
        - scope="session" means runs once for entire test run
        - Don't need to pass to test functions
    
    In Real Project:
        Replace with actual database setup:
        - Connect to test DB
        - Run migrations
        - Seed from fixtures
        - Use SQLAlchemy, psycopg2, etc.
    """
    global _test_db
    
    logger.info("="*60)
    logger.info("SETTING UP TEST DATABASE")
    logger.info("="*60)
    
    # Create test database
    _test_db = TestDatabase("test_automation_db")
    
    # Create tables
    logger.info("Creating tables...")
    
    _test_db.create_table("users", {
        "id": "integer",
        "email": "string",
        "password": "string",
        "username": "string",
        "role": "string"
    })
    
    _test_db.create_table("products", {
        "id": "integer",
        "name": "string",
        "price": "float",
        "stock": "integer"
    })
    
    _test_db.create_table("orders", {
        "id": "integer",
        "user_id": "integer",
        "product_id": "integer",
        "quantity": "integer",
        "status": "string"
    })
    
    # Seed initial data
    logger.info("Seeding test data...")
    
    # Test users
    _test_db.insert("users", {
        "id": 1,
        "email": "user@example.com",
        "password": "hashed_password_123",
        "username": "testuser",
        "role": "user"
    })
    
    _test_db.insert("users", {
        "id": 2,
        "email": "admin@example.com",
        "password": "hashed_admin_password",
        "username": "admin",
        "role": "admin"
    })
    
    # Test products
    _test_db.insert("products", {
        "id": 1,
        "name": "Laptop",
        "price": 999.99,
        "stock": 10
    })
    
    _test_db.insert("products", {
        "id": 2,
        "name": "Mouse",
        "price": 29.99,
        "stock": 50
    })
    
    logger.info("Test database setup completed")
    logger.info("="*60)
    
    yield  # All tests run here
    
    # Cleanup after tests
    logger.info("="*60)
    logger.info("TEARING DOWN TEST DATABASE")
    logger.info("="*60)
    
    # Drop tables
    _test_db.drop_table("orders")
    _test_db.drop_table("products")
    _test_db.drop_table("users")
    
    # Close connection
    _test_db.close()
    
    logger.info("Test database teardown completed")
    logger.info("="*60)


@pytest.fixture(scope="function")
def test_db():
    """
    Get test database connection (function scope).
    
    Yields:
        TestDatabase: Database instance for this test
    
    Notes:
        - Available to each test function
        - Can query/insert test data
        - Automatically cleaned up after test
    
    Usage:
        def test_login(test_db):
            users = test_db.query("users", email="user@example.com")
            assert len(users) > 0
    """
    global _test_db
    
    if _test_db is None:
        raise RuntimeError("Test database not initialized. setup_test_database fixture failed.")
    
    yield _test_db
    
    # Optional: Clear data after each test
    # _test_db.delete_all("orders")
    # logger.debug("Cleaned orders table")


@pytest.fixture(scope="function")
def reset_test_data():
    """
    Reset test data before each test (optional).
    
    Use if you want clean slate for each test.
    
    Usage:
        def test_something(reset_test_data, test_db):
            # test_db is clean here
            pass
    """
    global _test_db
    
    logger.info("Resetting test data for this test")
    
    # Clear all tables
    if _test_db:
        _test_db.delete_all("orders")
        _test_db.delete_all("products")
        _test_db.delete_all("users")
        
        # Re-seed initial data
        _test_db.insert("users", {
            "id": 1,
            "email": "user@example.com",
            "password": "hashed_password_123",
            "username": "testuser",
            "role": "user"
        })
        
        logger.debug("Test data reset completed")
    
    yield

