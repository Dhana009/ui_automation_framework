"""
Order Factory

Generate unique test orders for data-driven testing.
Use for creating test orders without data conflicts.
"""

import uuid
import random
from datetime import datetime
from utils.logger import get_logger

logger = get_logger(__name__)


class OrderFactory:
    """Factory for creating unique test orders"""
    
    STATUSES = ["pending", "processing", "shipped", "delivered", "cancelled"]
    
    @staticmethod
    def create_order(user_id: int = None, product_id: int = None, quantity: int = None, 
                     status: str = None) -> dict:
        """
        Create unique order with random data.
        
        Args:
            user_id: User ID (if None, random)
            product_id: Product ID (if None, random)
            quantity: Order quantity (if None, random 1-10)
            status: Order status (if None, random)
        
        Returns:
            Dictionary with order data
            
        Example:
            order = OrderFactory.create_order(user_id=1, product_id=10)
            # Returns: {
            #   'order_id': 'ORD_abc123',
            #   'user_id': 1,
            #   'product_id': 10,
            #   'quantity': 5,
            #   'unit_price': 99.99,
            #   'total_price': 499.95,
            #   'status': 'pending',
            #   'created_at': '2025-12-17T...',
            #   'updated_at': '2025-12-17T...'
            # }
        """
        unique_id = str(uuid.uuid4())[:6]
        
        if user_id is None:
            user_id = random.randint(1, 100)
        
        if product_id is None:
            product_id = random.randint(1, 50)
        
        if quantity is None:
            quantity = random.randint(1, 10)
        
        if status is None:
            status = random.choice(OrderFactory.STATUSES)
        
        unit_price = round(random.uniform(10, 500), 2)
        total_price = round(unit_price * quantity, 2)
        
        order = {
            'order_id': f'ORD_{unique_id}',
            'user_id': user_id,
            'product_id': product_id,
            'quantity': quantity,
            'unit_price': unit_price,
            'total_price': total_price,
            'status': status,
            'shipping_address': f'123 Main St, City {random.randint(1000, 9999)}',
            'payment_method': random.choice(['credit_card', 'paypal', 'bank_transfer']),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        logger.info(f"Created order: {order['order_id']} - user {user_id}, quantity {quantity}")
        return order
    
    @staticmethod
    def create_pending_order(user_id: int = None, product_id: int = None) -> dict:
        """Create pending order"""
        return OrderFactory.create_order(user_id=user_id, product_id=product_id, status="pending")
    
    @staticmethod
    def create_shipped_order(user_id: int = None, product_id: int = None) -> dict:
        """Create shipped order"""
        return OrderFactory.create_order(user_id=user_id, product_id=product_id, status="shipped")
    
    @staticmethod
    def create_delivered_order(user_id: int = None, product_id: int = None) -> dict:
        """Create delivered order"""
        return OrderFactory.create_order(user_id=user_id, product_id=product_id, status="delivered")
    
    @staticmethod
    def create_cancelled_order(user_id: int = None, product_id: int = None) -> dict:
        """Create cancelled order"""
        return OrderFactory.create_order(user_id=user_id, product_id=product_id, status="cancelled")
    
    @staticmethod
    def create_batch_orders(count: int, user_id: int = None) -> list:
        """
        Create multiple unique orders.
        
        Args:
            count: Number of orders to create
            user_id: User ID (optional, if None random for each)
        
        Returns:
            List of order dictionaries
            
        Example:
            orders = OrderFactory.create_batch_orders(5, user_id=1)
        """
        orders = [OrderFactory.create_order(user_id=user_id) for _ in range(count)]
        logger.info(f"Created batch of {count} orders")
        return orders
    
    @staticmethod
    def create_orders_for_user(user_id: int, count: int) -> list:
        """
        Create multiple orders for specific user.
        
        Args:
            user_id: User ID
            count: Number of orders
        
        Returns:
            List of order dictionaries
            
        Example:
            orders = OrderFactory.create_orders_for_user(user_id=1, count=3)
        """
        orders = [OrderFactory.create_order(user_id=user_id) for _ in range(count)]
        logger.info(f"Created {count} orders for user {user_id}")
        return orders
    
    @staticmethod
    def create_order_with_custom_data(order_id: str, user_id: int, product_id: int, 
                                     quantity: int, **kwargs) -> dict:
        """
        Create order with custom data.
        
        Args:
            order_id: Order ID
            user_id: User ID
            product_id: Product ID
            quantity: Quantity
            **kwargs: Additional order fields
        
        Returns:
            Dictionary with order data
            
        Example:
            order = OrderFactory.create_order_with_custom_data(
                order_id="ORD-001",
                user_id=1,
                product_id=10,
                quantity=5,
                status="shipped"
            )
        """
        unit_price = round(random.uniform(10, 500), 2)
        
        order = {
            'order_id': order_id,
            'user_id': user_id,
            'product_id': product_id,
            'quantity': quantity,
            'unit_price': unit_price,
            'total_price': round(unit_price * quantity, 2),
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        order.update(kwargs)
        logger.info(f"Created custom order: {order_id}")
        return order

