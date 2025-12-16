"""
User Factory

Generate unique test users for data-driven testing.
Use for creating test accounts without conflicts in parallel execution.
"""

import uuid
import random
from datetime import datetime
from utils.logger import get_logger

logger = get_logger(__name__)


class UserFactory:
    """Factory for creating unique test users"""
    
    @staticmethod
    def create_user(role: str = "user", email_domain: str = "testuser.com") -> dict:
        """
        Create unique user with random data.
        
        Args:
            role: User role (user, admin, moderator, guest)
            email_domain: Email domain for user
        
        Returns:
            Dictionary with user data
            
        Example:
            user = UserFactory.create_user(role="admin")
            # Returns: {
            #   'email': 'user_abc123@testuser.com',
            #   'password': 'SecurePass123!',
            #   'username': 'testuser_12345',
            #   'first_name': 'John',
            #   'last_name': 'Doe',
            #   'role': 'admin',
            #   'phone': '+1-555-0123'
            # }
        """
        unique_id = str(uuid.uuid4())[:8]
        random_num = random.randint(1000, 9999)
        
        user = {
            'email': f'user_{unique_id}@{email_domain}',
            'password': 'SecurePass123!',
            'username': f'testuser_{random_num}',
            'first_name': f'FirstName_{random_num}',
            'last_name': f'LastName_{random_num}',
            'role': role,
            'phone': f'+1-555-{random_num}',
            'created_at': datetime.now().isoformat(),
            'is_active': True
        }
        
        logger.info(f"Created user: {user['email']}")
        return user
    
    @staticmethod
    def create_admin_user() -> dict:
        """Create admin user"""
        return UserFactory.create_user(role="admin")
    
    @staticmethod
    def create_guest_user() -> dict:
        """Create guest user"""
        return UserFactory.create_user(role="guest")
    
    @staticmethod
    def create_batch_users(count: int, role: str = "user") -> list:
        """
        Create multiple unique users.
        
        Args:
            count: Number of users to create
            role: Role for all users
        
        Returns:
            List of user dictionaries
            
        Example:
            users = UserFactory.create_batch_users(5)
        """
        users = [UserFactory.create_user(role=role) for _ in range(count)]
        logger.info(f"Created batch of {count} users")
        return users
    
    @staticmethod
    def create_user_with_custom_data(email: str, password: str, **kwargs) -> dict:
        """
        Create user with custom data.
        
        Args:
            email: User email
            password: User password
            **kwargs: Additional user fields
        
        Returns:
            Dictionary with user data
            
        Example:
            user = UserFactory.create_user_with_custom_data(
                email="custom@example.com",
                password="CustomPass123",
                first_name="John",
                last_name="Doe"
            )
        """
        user = {
            'email': email,
            'password': password,
            'username': email.split('@')[0],
            'created_at': datetime.now().isoformat(),
            'is_active': True
        }
        
        user.update(kwargs)
        logger.info(f"Created custom user: {email}")
        return user

