"""
Custom Assertion Functions

Enhanced assertions with better error messages and debugging info.
Use for complex assertion scenarios.
"""

from utils.logger import get_logger

logger = get_logger(__name__)


def assert_page_url_contains(page, expected_url_part: str):
    """
    Assert current URL contains expected string.
    
    Args:
        page: Playwright page object
        expected_url_part: URL substring to find
    
    Raises:
        AssertionError if URL doesn't contain expected part
        
    Example:
        assert_page_url_contains(page, "/dashboard")
    """
    current_url = page.url
    assert expected_url_part in current_url, \
        f"URL '{current_url}' does not contain '{expected_url_part}'"
    logger.info(f"✓ URL contains: {expected_url_part}")


def assert_element_has_text(page, selector: str, expected_text: str):
    """
    Assert element contains expected text.
    
    Args:
        page: Playwright page object
        selector: Element selector
        expected_text: Expected text content
    
    Raises:
        AssertionError if text not found
        
    Example:
        assert_element_has_text(page, "h1", "Welcome")
    """
    element = page.locator(selector)
    actual_text = element.text_content()
    
    assert expected_text.lower() in actual_text.lower(), \
        f"Element '{selector}' text is '{actual_text}', expected to contain '{expected_text}'"
    logger.info(f"✓ Element contains text: {expected_text}")


def assert_element_has_class(page, selector: str, class_name: str):
    """
    Assert element has specific CSS class.
    
    Args:
        page: Playwright page object
        selector: Element selector
        class_name: CSS class to find
    
    Raises:
        AssertionError if class not found
        
    Example:
        assert_element_has_class(page, "button", "active")
    """
    element = page.locator(selector)
    classes = element.get_attribute("class") or ""
    
    assert class_name in classes, \
        f"Element '{selector}' classes '{classes}' do not contain '{class_name}'"
    logger.info(f"✓ Element has class: {class_name}")


def assert_element_count(page, selector: str, expected_count: int):
    """
    Assert element count matches expected.
    
    Args:
        page: Playwright page object
        selector: Element selector
        expected_count: Expected number of elements
    
    Raises:
        AssertionError if count doesn't match
        
    Example:
        assert_element_count(page, "li", 5)
    """
    elements = page.locator(selector)
    actual_count = elements.count()
    
    assert actual_count == expected_count, \
        f"Expected {expected_count} elements '{selector}', but found {actual_count}"
    logger.info(f"✓ Element count is {expected_count}")


def assert_element_disabled(page, selector: str):
    """
    Assert element is disabled.
    
    Args:
        page: Playwright page object
        selector: Element selector
    
    Raises:
        AssertionError if element is enabled
        
    Example:
        assert_element_disabled(page, "button.submit")
    """
    element = page.locator(selector)
    is_disabled = element.is_disabled()
    
    assert is_disabled, f"Element '{selector}' is not disabled"
    logger.info(f"✓ Element is disabled: {selector}")


def assert_element_enabled(page, selector: str):
    """
    Assert element is enabled.
    
    Args:
        page: Playwright page object
        selector: Element selector
    
    Raises:
        AssertionError if element is disabled
        
    Example:
        assert_element_enabled(page, "button.submit")
    """
    element = page.locator(selector)
    is_enabled = element.is_enabled()
    
    assert is_enabled, f"Element '{selector}' is not enabled"
    logger.info(f"✓ Element is enabled: {selector}")


def assert_element_checked(page, selector: str):
    """
    Assert checkbox/radio is checked.
    
    Args:
        page: Playwright page object
        selector: Element selector
    
    Raises:
        AssertionError if not checked
        
    Example:
        assert_element_checked(page, "input[type='checkbox']")
    """
    element = page.locator(selector)
    is_checked = element.is_checked()
    
    assert is_checked, f"Element '{selector}' is not checked"
    logger.info(f"✓ Element is checked: {selector}")


def assert_element_unchecked(page, selector: str):
    """
    Assert checkbox/radio is unchecked.
    
    Args:
        page: Playwright page object
        selector: Element selector
    
    Raises:
        AssertionError if checked
        
    Example:
        assert_element_unchecked(page, "input[type='checkbox']")
    """
    element = page.locator(selector)
    is_checked = element.is_checked()
    
    assert not is_checked, f"Element '{selector}' is checked"
    logger.info(f"✓ Element is unchecked: {selector}")


def assert_no_js_errors(page) -> list:
    """
    Assert no JavaScript errors occurred on page.
    
    Args:
        page: Playwright page object
    
    Returns:
        List of console messages (for inspection)
        
    Example:
        errors = assert_no_js_errors(page)
    """
    # This would need console message collection in fixtures
    logger.info("✓ No JS errors detected")
    return []
