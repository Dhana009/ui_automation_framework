"""
Product Factory

Generate unique test products for data-driven testing.
Use for creating test products without inventory conflicts.
"""

import uuid
import random
from datetime import datetime
from utils.logger import get_logger

logger = get_logger(__name__)


class ProductFactory:
    """Factory for creating unique test products"""
    
    CATEGORIES = ["Electronics", "Clothing", "Books", "Sports", "Home", "Beauty"]
    
    @staticmethod
    def create_product(category: str = None, in_stock: bool = True) -> dict:
        """
        Create unique product with random data.
        
        Args:
            category: Product category
            in_stock: Whether product is in stock
        
        Returns:
            Dictionary with product data
            
        Example:
            product = ProductFactory.create_product(category="Electronics")
            # Returns: {
            #   'sku': 'SKU_abc123',
            #   'name': 'Product_5678',
            #   'description': 'Test product',
            #   'price': 99.99,
            #   'category': 'Electronics',
            #   'stock': 50,
            #   'in_stock': True,
            #   'created_at': '2025-12-17T...'
            # }
        """
        unique_id = str(uuid.uuid4())[:6]
        random_num = random.randint(1000, 9999)
        
        if category is None:
            category = random.choice(ProductFactory.CATEGORIES)
        
        stock = random.randint(10, 100) if in_stock else 0
        
        product = {
            'sku': f'SKU_{unique_id}',
            'name': f'Product_{random_num}',
            'description': f'Test product {random_num}',
            'price': round(random.uniform(10, 1000), 2),
            'category': category,
            'stock': stock,
            'in_stock': in_stock,
            'rating': round(random.uniform(1, 5), 1),
            'reviews': random.randint(0, 100),
            'created_at': datetime.now().isoformat()
        }
        
        logger.info(f"Created product: {product['sku']} - {product['name']}")
        return product
    
    @staticmethod
    def create_electronics() -> dict:
        """Create electronics product"""
        return ProductFactory.create_product(category="Electronics")
    
    @staticmethod
    def create_clothing() -> dict:
        """Create clothing product"""
        return ProductFactory.create_product(category="Clothing")
    
    @staticmethod
    def create_book() -> dict:
        """Create book product"""
        return ProductFactory.create_product(category="Books")
    
    @staticmethod
    def create_out_of_stock_product() -> dict:
        """Create out of stock product"""
        return ProductFactory.create_product(in_stock=False)
    
    @staticmethod
    def create_batch_products(count: int, category: str = None) -> list:
        """
        Create multiple unique products.
        
        Args:
            count: Number of products to create
            category: Product category (optional)
        
        Returns:
            List of product dictionaries
            
        Example:
            products = ProductFactory.create_batch_products(5, category="Electronics")
        """
        products = [ProductFactory.create_product(category=category) for _ in range(count)]
        logger.info(f"Created batch of {count} products")
        return products
    
    @staticmethod
    def create_product_with_custom_data(sku: str, name: str, price: float, **kwargs) -> dict:
        """
        Create product with custom data.
        
        Args:
            sku: Product SKU
            name: Product name
            price: Product price
            **kwargs: Additional product fields
        
        Returns:
            Dictionary with product data
            
        Example:
            product = ProductFactory.create_product_with_custom_data(
                sku="SKU-001",
                name="Custom Product",
                price=99.99,
                category="Electronics",
                stock=50
            )
        """
        product = {
            'sku': sku,
            'name': name,
            'price': price,
            'stock': 50,
            'in_stock': True,
            'created_at': datetime.now().isoformat()
        }
        
        product.update(kwargs)
        logger.info(f"Created custom product: {sku} - {name}")
        return product

