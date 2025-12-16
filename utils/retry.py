"""
Retry Decorators and Functions

Retry logic for handling transient failures and flaky operations.
"""

import functools
import time
from typing import Callable, Any
from utils.logger import get_logger

logger = get_logger(__name__)


def retry(max_attempts: int = 3, delay: float = 2, backoff: float = 1.0):
    """
    Decorator to retry a function on failure.
    
    Args:
        max_attempts: Maximum retry attempts
        delay: Delay between retries in seconds
        backoff: Multiplier for delay each retry (1.0 = constant, 2.0 = exponential)
    
    Example:
        @retry(max_attempts=3, delay=2)
        def flaky_operation():
            # Do something that might fail
            pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            current_delay = delay
            
            for attempt in range(1, max_attempts + 1):
                try:
                    logger.info(f"Executing {func.__name__} (attempt {attempt}/{max_attempts})")
                    result = func(*args, **kwargs)
                    
                    if attempt > 1:
                        logger.info(f"✓ {func.__name__} succeeded on attempt {attempt}")
                    
                    return result
                
                except Exception as e:
                    last_exception = e
                    
                    if attempt < max_attempts:
                        logger.warning(f"Attempt {attempt} failed: {str(e)}")
                        logger.info(f"Retrying in {current_delay}s...")
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(f"All {max_attempts} attempts failed")
            
            raise last_exception
        
        return wrapper
    return decorator


def retry_on_exception(exception_type: type, max_attempts: int = 3, delay: float = 2):
    """
    Decorator to retry only on specific exception type.
    
    Args:
        exception_type: Exception class to catch and retry
        max_attempts: Maximum retry attempts
        delay: Delay between retries in seconds
    
    Example:
        @retry_on_exception(TimeoutError, max_attempts=3)
        def network_call():
            # Do something that might timeout
            pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                
                except exception_type as e:
                    if attempt < max_attempts:
                        logger.warning(f"{exception_type.__name__} on attempt {attempt}, retrying...")
                        time.sleep(delay)
                    else:
                        logger.error(f"Failed after {max_attempts} attempts")
                        raise
        
        return wrapper
    return decorator


def retry_with_timeout(max_attempts: int = 3, timeout_per_attempt: float = 5):
    """
    Decorator to retry with timeout on each attempt.
    
    Args:
        max_attempts: Maximum retry attempts
        timeout_per_attempt: Timeout for each attempt in seconds
    
    Example:
        @retry_with_timeout(max_attempts=3, timeout_per_attempt=10)
        def slow_operation():
            # Do something that might be slow
            pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(1, max_attempts + 1):
                try:
                    start_time = time.time()
                    result = func(*args, **kwargs)
                    elapsed = time.time() - start_time
                    
                    logger.info(f"{func.__name__} completed in {elapsed:.2f}s")
                    return result
                
                except Exception as e:
                    elapsed = time.time() - start_time
                    
                    if elapsed > timeout_per_attempt:
                        logger.error(f"Operation timeout: {elapsed:.2f}s > {timeout_per_attempt}s")
                    
                    if attempt < max_attempts:
                        logger.warning(f"Attempt {attempt} failed, retrying...")
                        time.sleep(1)
                    else:
                        raise
        
        return wrapper
    return decorator


def mark_flaky(func: Callable) -> Callable:
    """
    Decorator to mark test as flaky (for future flaky detection system).
    
    Example:
        @mark_flaky
        def test_something():
            # Test that might fail intermittently
            pass
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.warning(f"Test marked as FLAKY: {func.__name__}")
        return func(*args, **kwargs)
    
    # Store metadata for flaky detection
    wrapper._is_flaky = True
    return wrapper


def retry_function(func: Callable, *args, max_attempts: int = 3, delay: float = 1, **kwargs) -> Any:
    """
    Retry a function call programmatically (without decorator).
    
    Args:
        func: Function to call
        args: Positional arguments
        max_attempts: Maximum attempts
        delay: Delay between retries
        kwargs: Keyword arguments
    
    Returns:
        Function result
    
    Example:
        result = retry_function(my_function, arg1, arg2, max_attempts=3)
    """
    last_exception = None
    
    for attempt in range(1, max_attempts + 1):
        try:
            logger.info(f"Executing {func.__name__} (attempt {attempt}/{max_attempts})")
            return func(*args, **kwargs)
        
        except Exception as e:
            last_exception = e
            
            if attempt < max_attempts:
                logger.warning(f"Attempt failed: {str(e)}, retrying in {delay}s...")
                time.sleep(delay)
            else:
                logger.error(f"All attempts failed")
    
    raise last_exception
