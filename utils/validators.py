"""
Data Validation Functions

Validate test data, user inputs, and responses.
"""

import re
from typing import Any
from utils.logger import get_logger

logger = get_logger(__name__)


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email string to validate
    
    Returns:
        True if valid, False otherwise
        
    Example:
        assert validate_email("user@example.com")
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    is_valid = re.match(pattern, email) is not None
    
    logger.info(f"Email validation: {email} - {is_valid}")
    return is_valid


def validate_password(password: str, min_length: int = 8) -> bool:
    """
    Validate password strength.
    
    Args:
        password: Password to validate
        min_length: Minimum password length
    
    Returns:
        True if valid, False otherwise
        
    Example:
        assert validate_password("SecurePass123!")
    """
    if len(password) < min_length:
        logger.warning(f"Password too short: {len(password)} < {min_length}")
        return False
    
    # Check for uppercase, lowercase, number, special char
    has_upper = re.search(r'[A-Z]', password) is not None
    has_lower = re.search(r'[a-z]', password) is not None
    has_digit = re.search(r'\d', password) is not None
    
    is_valid = has_upper and has_lower and has_digit
    logger.info(f"Password validation: {is_valid}")
    
    return is_valid


def validate_url(url: str) -> bool:
    """
    Validate URL format.
    
    Args:
        url: URL string to validate
    
    Returns:
        True if valid, False otherwise
        
    Example:
        assert validate_url("https://example.com/path")
    """
    pattern = r'^https?://[\w.-]+(:\d+)?(/[\w./?%&=]*)?$'
    is_valid = re.match(pattern, url) is not None
    
    logger.info(f"URL validation: {url} - {is_valid}")
    return is_valid


def validate_phone(phone: str) -> bool:
    """
    Validate phone number format (US format).
    
    Args:
        phone: Phone number to validate
    
    Returns:
        True if valid, False otherwise
        
    Example:
        assert validate_phone("+1-555-0123")
    """
    # Accepts formats: +1-555-0123, (555) 0123, 555 0123, etc.
    pattern = r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'
    is_valid = re.match(pattern, phone.replace(" ", "")) is not None
    
    logger.info(f"Phone validation: {phone} - {is_valid}")
    return is_valid


def validate_credit_card(card_number: str) -> bool:
    """
    Validate credit card number using Luhn algorithm.
    
    Args:
        card_number: Card number (digits only)
    
    Returns:
        True if valid, False otherwise
        
    Example:
        assert validate_credit_card("4532015112830366")
    """
    # Remove non-digits
    card = re.sub(r'\D', '', card_number)
    
    # Check length (13-19 digits)
    if len(card) < 13 or len(card) > 19:
        logger.warning(f"Card length invalid: {len(card)}")
        return False
    
    # Luhn algorithm
    def luhn_checksum(card):
        def digits_of(n):
            return [int(d) for d in str(n)]
        
        digits = digits_of(card)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        
        return checksum % 10
    
    is_valid = luhn_checksum(card) == 0
    logger.info(f"Card validation: {is_valid}")
    
    return is_valid


def validate_not_empty(value: Any) -> bool:
    """
    Validate value is not empty.
    
    Args:
        value: Value to validate
    
    Returns:
        True if not empty, False otherwise
        
    Example:
        assert validate_not_empty("some value")
    """
    is_valid = value is not None and str(value).strip() != ""
    logger.info(f"Not empty validation: {is_valid}")
    return is_valid


def validate_length(value: str, min_length: int = None, max_length: int = None) -> bool:
    """
    Validate string length.
    
    Args:
        value: String to validate
        min_length: Minimum length (optional)
        max_length: Maximum length (optional)
    
    Returns:
        True if valid, False otherwise
        
    Example:
        assert validate_length("username", min_length=3, max_length=20)
    """
    length = len(value)
    
    if min_length is not None and length < min_length:
        logger.warning(f"Length too short: {length} < {min_length}")
        return False
    
    if max_length is not None and length > max_length:
        logger.warning(f"Length too long: {length} > {max_length}")
        return False
    
    logger.info(f"Length validation: {length} - valid")
    return True


def validate_matches_pattern(value: str, pattern: str) -> bool:
    """
    Validate value matches regex pattern.
    
    Args:
        value: Value to validate
        pattern: Regex pattern
    
    Returns:
        True if matches, False otherwise
        
    Example:
        assert validate_matches_pattern("ABC123", r'^[A-Z]{3}\d{3}$')
    """
    is_valid = re.match(pattern, value) is not None
    logger.info(f"Pattern validation: {is_valid}")
    return is_valid
