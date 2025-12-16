"""
Custom Function Decorators

Decorators for logging, performance, error handling, and more.
"""

import functools
import time
from typing import Callable, Any
from utils.logger import get_logger

logger = get_logger(__name__)


def log_execution(func: Callable) -> Callable:
    """
    Decorator to log function execution with timing.
    
    Example:
        @log_execution
        def test_login():
            pass
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        logger.info(f"{'='*60}")
        logger.info(f"EXECUTING: {func.__name__}")
        logger.info(f"{'='*60}")
        
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            
            logger.info(f"✓ COMPLETED: {func.__name__} ({elapsed:.2f}s)")
            logger.info(f"{'='*60}")
            
            return result
        
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"✗ FAILED: {func.__name__} ({elapsed:.2f}s)")
            logger.error(f"Error: {str(e)}")
            logger.error(f"{'='*60}")
            raise
    
    return wrapper


def measure_performance(func: Callable) -> Callable:
    """
    Decorator to measure and log function performance.
    
    Example:
        @measure_performance
        def slow_operation():
            pass
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start_time
        
        # Categorize performance
        if elapsed < 1:
            level = "FAST"
        elif elapsed < 5:
            level = "NORMAL"
        elif elapsed < 10:
            level = "SLOW"
        else:
            level = "VERY_SLOW"
        
        logger.info(f"[{level}] {func.__name__}: {elapsed:.2f}s")
        
        return result
    
    return wrapper


def catch_stale_element(func: Callable) -> Callable:
    """
    Decorator to catch and handle stale element exceptions.
    
    Example:
        @catch_stale_element
        def interact_with_element():
            pass
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        max_retries = 2
        
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            
            except Exception as e:
                if "stale" in str(e).lower() and attempt < max_retries - 1:
                    logger.warning(f"Stale element detected, retrying...")
                    time.sleep(0.5)
                else:
                    raise
    
    return wrapper


def skip_on_exception(exception_type: type = Exception, log_message: str = "Skipping"):
    """
    Decorator to skip execution if exception occurs.
    
    Example:
        @skip_on_exception(TimeoutError)
        def test_something():
            pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            
            except exception_type as e:
                logger.warning(f"{log_message}: {str(e)}")
                return None
        
        return wrapper
    return decorator


def timeout(seconds: float):
    """
    Decorator to timeout function execution (requires signal module).
    
    Note: This is a reference decorator. Full implementation requires signal module.
    
    Example:
        @timeout(30)
        def long_operation():
            pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            logger.info(f"Executing with {seconds}s timeout: {func.__name__}")
            
            # Simple implementation using time check
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            
            if elapsed > seconds:
                logger.warning(f"Function exceeded timeout: {elapsed:.2f}s > {seconds}s")
            
            return result
        
        return wrapper
    return decorator


def retry_on_fail(max_attempts: int = 3, delay: float = 1):
    """
    Decorator to retry function on failure.
    
    Example:
        @retry_on_fail(max_attempts=3)
        def flaky_operation():
            pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    if attempt > 1:
                        logger.info(f"Retry attempt {attempt}/{max_attempts}")
                    
                    return func(*args, **kwargs)
                
                except Exception as e:
                    last_exception = e
                    
                    if attempt < max_attempts:
                        logger.warning(f"Attempt {attempt} failed, retrying in {delay}s...")
                        time.sleep(delay)
                    else:
                        logger.error(f"All {max_attempts} attempts failed")
            
            raise last_exception
        
        return wrapper
    return decorator


def screenshot_on_error(page_obj=None):
    """
    Decorator to take screenshot on function error.
    
    Example:
        @screenshot_on_error()
        def test_something(page):
            pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {str(e)}")
                
                # If page object passed, take screenshot
                if page_obj:
                    try:
                        page_obj.screenshot(path=f"screenshots/{func.__name__}_error.png")
                        logger.error(f"Screenshot saved: {func.__name__}_error.png")
                    except:
                        pass
                
                raise
        
        return wrapper
    return decorator
