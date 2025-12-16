"""
Custom Wait Functions

Extended wait strategies beyond BasePage.
Use for complex waiting scenarios.
"""

import time
from typing import Callable
from utils.logger import get_logger

logger = get_logger(__name__)


def wait_for_condition(condition_fn: Callable, timeout: int = 10, poll_interval: float = 0.5) -> bool:
    """
    Wait for a custom condition to become true.
    
    Args:
        condition_fn: Function that returns True when condition met
        timeout: Maximum wait time in seconds
        poll_interval: How often to check condition
    
    Returns:
        True if condition met, False if timeout
        
    Example:
        def is_element_count_correct():
            return len(page.locator("button")) == 5
        
        wait_for_condition(is_element_count_correct, timeout=10)
    """
    logger.info(f"Waiting for condition (timeout: {timeout}s)")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            if condition_fn():
                logger.info("Condition met")
                return True
        except Exception as e:
            logger.debug(f"Condition check failed: {e}")
        
        time.sleep(poll_interval)
    
    logger.warning(f"Condition timeout after {timeout}s")
    return False


def wait_for_element_count(page, selector: str, expected_count: int, timeout: int = 10) -> bool:
    """
    Wait for element count to reach expected number.
    
    Args:
        page: Playwright page object
        selector: Element selector
        expected_count: Expected number of elements
        timeout: Maximum wait in seconds
    
    Returns:
        True if count reached, False if timeout
        
    Example:
        wait_for_element_count(page, "button", 5)
    """
    logger.info(f"Waiting for {expected_count} elements: {selector}")
    
    def check_count():
        count = page.locator(selector).count()
        return count == expected_count
    
    return wait_for_condition(check_count, timeout)


def wait_for_text_change(page, selector: str, initial_text: str, timeout: int = 10) -> bool:
    """
    Wait for element text to change from initial value.
    
    Args:
        page: Playwright page object
        selector: Element selector
        initial_text: Original text value
        timeout: Maximum wait in seconds
    
    Returns:
        True if text changed, False if timeout
        
    Example:
        wait_for_text_change(page, ".status", "Loading...")
    """
    logger.info(f"Waiting for text change on: {selector}")
    
    def text_changed():
        current_text = page.locator(selector).text_content()
        changed = current_text != initial_text
        if changed:
            logger.debug(f"Text changed from '{initial_text}' to '{current_text}'")
        return changed
    
    return wait_for_condition(text_changed, timeout)


def wait_for_attribute_value(page, selector: str, attribute: str, value: str, timeout: int = 10) -> bool:
    """
    Wait for element attribute to have specific value.
    
    Args:
        page: Playwright page object
        selector: Element selector
        attribute: Attribute name
        value: Expected attribute value
        timeout: Maximum wait in seconds
    
    Returns:
        True if attribute has value, False if timeout
        
    Example:
        wait_for_attribute_value(page, "button", "disabled", "true")
    """
    logger.info(f"Waiting for {attribute}='{value}' on: {selector}")
    
    def attribute_matches():
        actual = page.locator(selector).get_attribute(attribute)
        match = actual == value
        if match:
            logger.debug(f"Attribute '{attribute}' is '{value}'")
        return match
    
    return wait_for_condition(attribute_matches, timeout)


def wait_for_multiple_elements_visible(page, selectors: list, timeout: int = 10) -> bool:
    """
    Wait for all elements in list to be visible.
    
    Args:
        page: Playwright page object
        selectors: List of element selectors
        timeout: Maximum wait in seconds
    
    Returns:
        True if all visible, False if timeout
        
    Example:
        wait_for_multiple_elements_visible(page, [".header", ".content", ".footer"])
    """
    logger.info(f"Waiting for {len(selectors)} elements to be visible")
    
    def all_visible():
        for selector in selectors:
            if not page.locator(selector).is_visible():
                return False
        return True
    
    return wait_for_condition(all_visible, timeout)
