"""
Base Page Class

Foundation class for all page objects.
Contains common methods used by all pages (click, type, wait, assert, etc.)
Implements self-healing patterns (explicit waits, retries, element re-location).

All page objects should inherit from this class.

Usage:
    from pages.base_page import BasePage
    
    class LoginPage(BasePage):
        def login(self, email, password):
            self.type_text("input[name='email']", email)
            self.click("button[type='submit']")
"""

import time
from pathlib import Path
from config.settings import config
from utils.logger import get_logger

logger = get_logger(__name__)


class BasePage:
    """
    Base page class for all page objects.
    Provides common interactions: click, type, wait, assert, etc.
    Automatically implements self-healing patterns.
    """
    
    def __init__(self, page):
        """
        Initialize page with Playwright page object.
        
        Args:
            page: Playwright page object from browser context
        """
        self.page = page
        logger.info(f"Initialized {self.__class__.__name__}")
    
    # ==================== WAIT METHODS (Self-Healing #1) ====================
    
    def wait_for_element(self, selector: str, timeout: int = None, state: str = "attached"):
        """
        Wait for element to be in specified state (attached, visible, hidden).
        
        Args:
            selector: CSS selector or XPath for element
            timeout: Timeout in milliseconds (uses config if not provided)
            state: "attached" (default), "visible", or "hidden"
        
        Returns:
            None (raises exception if timeout)
        """
        timeout = timeout or config.timeouts["element_wait"] * 1000
        logger.info(f"Waiting for element: {selector} (state={state})")
        
        try:
            self.page.wait_for_selector(selector, state=state, timeout=timeout)
            logger.debug(f"Element found: {selector}")
        except Exception as e:
            logger.error(f"Element wait failed: {selector} - {str(e)}")
            raise
    
    def wait_for_element_visible(self, selector: str, timeout: int = None):
        """
        Wait for element to be visible (not just present in DOM).
        
        Args:
            selector: CSS selector or XPath
            timeout: Timeout in milliseconds
        """
        self.wait_for_element(selector, timeout, state="visible")
    
    def wait_for_element_hidden(self, selector: str, timeout: int = None):
        """
        Wait for element to be hidden.
        
        Args:
            selector: CSS selector or XPath
            timeout: Timeout in milliseconds
        """
        self.wait_for_element(selector, timeout, state="hidden")
    
    def wait_for_url(self, url_pattern: str, timeout: int = None):
        """
        Wait for URL to match pattern.
        
        Args:
            url_pattern: URL pattern (supports wildcards: **/dashboard)
            timeout: Timeout in milliseconds
        """
        timeout = timeout or config.timeouts["page_load"] * 1000
        logger.info(f"Waiting for URL: {url_pattern}")
        
        try:
            self.page.wait_for_url(url_pattern, timeout=timeout)
            logger.debug(f"URL matched: {url_pattern}")
        except Exception as e:
            logger.error(f"URL wait failed: {url_pattern} - {str(e)}")
            raise
    
    def wait_for_load_state(self, state: str = "networkidle", timeout: int = None):
        """
        Wait for page to reach load state (networkidle, load, domcontentloaded).
        
        Args:
            state: "networkidle" (default - all requests done), "load", "domcontentloaded"
            timeout: Timeout in milliseconds
        """
        timeout = timeout or config.timeouts["page_load"] * 1000
        logger.info(f"Waiting for page load state: {state}")
        
        try:
            self.page.wait_for_load_state(state, timeout=timeout)
            logger.debug(f"Page load state reached: {state}")
        except Exception as e:
            logger.error(f"Load state wait failed: {state} - {str(e)}")
            raise
    
    def wait_for_text(self, text: str, timeout: int = None):
        """
        Wait for text to appear anywhere on page.
        
        Args:
            text: Text to wait for
            timeout: Timeout in milliseconds
        """
        timeout = timeout or config.timeouts["element_wait"] * 1000
        logger.info(f"Waiting for text: {text}")
        
        try:
            self.page.wait_for_function(
                f"document.body.innerText.includes('{text}')",
                timeout=timeout
            )
            logger.debug(f"Text found: {text}")
        except Exception as e:
            logger.error(f"Text wait failed: {text} - {str(e)}")
            raise
    
    # ==================== INTERACTION METHODS (Self-Healing #2) ====================
    
    def click(self, selector: str, retry_count: int = 3):
        """
        Click element (always re-locate, never cache).
        Automatically retries if transient failure occurs.
        
        Args:
            selector: CSS selector or XPath
            retry_count: Number of retries on failure
        
        Note:
            Always re-locates element (doesn't cache reference)
            Waits for element to be clickable before clicking
            Retries on transient failures
        """
        for attempt in range(1, retry_count + 1):
            try:
                logger.info(f"Clicking element: {selector}")
                self.wait_for_element_visible(selector)  # Ensure visible
                self.page.click(selector)
                logger.debug(f"Element clicked: {selector}")
                return
            except Exception as e:
                if attempt == retry_count:
                    logger.error(f"Click failed after {retry_count} attempts: {selector} - {str(e)}")
                    raise
                logger.warning(f"Click attempt {attempt} failed, retrying...")
                time.sleep(1)
    
    def type_text(self, selector: str, text: str, clear_first: bool = True):
        """
        Type text into input field.
        Automatically waits for element and clears if needed.
        
        Args:
            selector: CSS selector or XPath of input element
            text: Text to type
            clear_first: Whether to clear field before typing (default: True)
        """
        logger.info(f"Typing text in element: {selector}")
        self.wait_for_element_visible(selector)
        
        if clear_first:
            self.page.fill(selector, "")  # Clear field
            logger.debug(f"Cleared field: {selector}")
        
        self.page.type(selector, text, delay=50)  # Delay for visibility
        logger.debug(f"Text typed: {selector} = {text[:20]}...")
    
    def fill_text(self, selector: str, text: str):
        """
        Fill input field (clear and type in one action).
        
        Args:
            selector: CSS selector or XPath
            text: Text to fill
        """
        logger.info(f"Filling text in element: {selector}")
        self.wait_for_element_visible(selector)
        self.page.fill(selector, text)
        logger.debug(f"Text filled: {selector}")
    
    def get_text(self, selector: str) -> str:
        """
        Get text content of element.
        
        Args:
            selector: CSS selector or XPath
        
        Returns:
            Text content of element
        """
        logger.info(f"Getting text from element: {selector}")
        self.wait_for_element_visible(selector)
        text = self.page.text_content(selector)
        logger.debug(f"Text retrieved: {text}")
        return text or ""
    
    def get_attribute(self, selector: str, attribute: str) -> str:
        """
        Get attribute value of element.
        
        Args:
            selector: CSS selector or XPath
            attribute: Attribute name (e.g., 'value', 'href', 'data-testid')
        
        Returns:
            Attribute value
        """
        logger.info(f"Getting attribute '{attribute}' from element: {selector}")
        self.wait_for_element(selector)
        value = self.page.get_attribute(selector, attribute)
        logger.debug(f"Attribute retrieved: {value}")
        return value or ""
    
    # ==================== VISIBILITY CHECKS (Self-Healing #3) ====================
    
    def is_visible(self, selector: str) -> bool:
        """
        Check if element is visible (not just exists in DOM).
        
        Args:
            selector: CSS selector or XPath
        
        Returns:
            True if visible, False otherwise
        """
        logger.debug(f"Checking if element visible: {selector}")
        try:
            return self.page.is_visible(selector)
        except Exception:
            return False
    
    def is_element_present(self, selector: str) -> bool:
        """
        Check if element exists in DOM (may not be visible).
        
        Args:
            selector: CSS selector or XPath
        
        Returns:
            True if present, False otherwise
        """
        logger.debug(f"Checking if element present: {selector}")
        try:
            element = self.page.query_selector(selector)
            return element is not None
        except Exception:
            return False
    
    def is_enabled(self, selector: str) -> bool:
        """
        Check if element is enabled (not disabled).
        
        Args:
            selector: CSS selector or XPath
        
        Returns:
            True if enabled, False otherwise
        """
        logger.debug(f"Checking if element enabled: {selector}")
        try:
            return self.page.is_enabled(selector)
        except Exception:
            return False
    
    def is_checked(self, selector: str) -> bool:
        """
        Check if checkbox/radio is checked.
        
        Args:
            selector: CSS selector or XPath
        
        Returns:
            True if checked, False otherwise
        """
        logger.debug(f"Checking if element checked: {selector}")
        try:
            return self.page.is_checked(selector)
        except Exception:
            return False
    
    # ==================== UTILITY METHODS ====================
    
    def scroll_to_element(self, selector: str):
        """
        Scroll element into view (handles sticky headers, etc.).
        
        Args:
            selector: CSS selector or XPath
        """
        logger.info(f"Scrolling to element: {selector}")
        self.page.locator(selector).scroll_into_view()
        logger.debug(f"Scrolled to element: {selector}")
    
    def hover(self, selector: str):
        """
        Hover over element (triggers hover effects).
        
        Args:
            selector: CSS selector or XPath
        """
        logger.info(f"Hovering over element: {selector}")
        self.wait_for_element_visible(selector)
        self.page.hover(selector)
        logger.debug(f"Hovered over element: {selector}")
    
    def take_screenshot(self, name: str = None):
        """
        Take screenshot and save to screenshots directory.
        
        Args:
            name: Screenshot name (auto-timestamped if not provided)
        
        Returns:
            Path to screenshot file
        """
        if name is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            name = f"screenshot_{timestamp}.png"
        
        screenshots_dir = Path(__file__).parent.parent / "screenshots"
        screenshots_dir.mkdir(exist_ok=True)
        
        filepath = screenshots_dir / name
        self.page.screenshot(path=str(filepath))
        logger.info(f"Screenshot saved: {filepath}")
        return str(filepath)
    
    def goto(self, url: str = None):
        """
        Navigate to URL.
        
        Args:
            url: Full URL to navigate to. If None, uses config.base_url
        """
        if url is None:
            url = config.base_url
        
        logger.info(f"Navigating to: {url}")
        self.page.goto(url)
        logger.debug(f"Navigated to: {url}")
    
    def reload(self):
        """Reload current page."""
        logger.info("Reloading page")
        self.page.reload()
    
    def go_back(self):
        """Go back to previous page."""
        logger.info("Going back to previous page")
        self.page.go_back()
    
    def go_forward(self):
        """Go forward to next page."""
        logger.info("Going forward to next page")
        self.page.go_forward()
    
    # ==================== PAGE STATE METHODS ====================
    
    def get_page_title(self) -> str:
        """
        Get page title.
        
        Returns:
            Page title
        """
        title = self.page.title()
        logger.debug(f"Page title: {title}")
        return title
    
    def get_current_url(self) -> str:
        """
        Get current page URL.
        
        Returns:
            Current URL
        """
        url = self.page.url
        logger.debug(f"Current URL: {url}")
        return url
    
    def get_page_source(self) -> str:
        """
        Get page HTML source.
        
        Returns:
            HTML source code
        """
        logger.info("Getting page source")
        return self.page.content()
    
    # ==================== FORM METHODS ====================
    
    def select_option(self, selector: str, value: str):
        """
        Select option from dropdown.
        
        Args:
            selector: CSS selector of select element
            value: Value to select
        """
        logger.info(f"Selecting option in dropdown: {selector} = {value}")
        self.wait_for_element_visible(selector)
        self.page.select_option(selector, value)
        logger.debug(f"Option selected: {value}")
    
    def check_checkbox(self, selector: str):
        """
        Check checkbox.
        
        Args:
            selector: CSS selector of checkbox
        """
        logger.info(f"Checking checkbox: {selector}")
        self.wait_for_element_visible(selector)
        if not self.is_checked(selector):
            self.click(selector)
        logger.debug(f"Checkbox checked: {selector}")
    
    def uncheck_checkbox(self, selector: str):
        """
        Uncheck checkbox.
        
        Args:
            selector: CSS selector of checkbox
        """
        logger.info(f"Unchecking checkbox: {selector}")
        self.wait_for_element_visible(selector)
        if self.is_checked(selector):
            self.click(selector)
        logger.debug(f"Checkbox unchecked: {selector}")
    
    # ==================== CUSTOM ASSERTIONS (Fail Safe) ====================
    
    def assert_element_visible(self, selector: str, message: str = None):
        """
        Assert element is visible.
        
        Args:
            selector: CSS selector
            message: Custom error message
        
        Raises:
            AssertionError if element not visible
        """
        logger.info(f"Asserting element visible: {selector}")
        if not self.is_visible(selector):
            error = message or f"Element not visible: {selector}"
            logger.error(error)
            raise AssertionError(error)
    
    def assert_text_contains(self, selector: str, expected_text: str):
        """
        Assert element text contains expected text.
        
        Args:
            selector: CSS selector
            expected_text: Text to find
        
        Raises:
            AssertionError if text not found
        """
        logger.info(f"Asserting text contains: {expected_text}")
        actual_text = self.get_text(selector)
        if expected_text not in actual_text:
            error = f"Expected '{expected_text}' in '{actual_text}'"
            logger.error(error)
            raise AssertionError(error)
    
    def assert_element_enabled(self, selector: str):
        """
        Assert element is enabled.
        
        Args:
            selector: CSS selector
        
        Raises:
            AssertionError if element disabled
        """
        logger.info(f"Asserting element enabled: {selector}")
        if not self.is_enabled(selector):
            error = f"Element not enabled: {selector}"
            logger.error(error)
            raise AssertionError(error)
    
    def assert_url_contains(self, expected_url: str):
        """
        Assert current URL contains expected string.
        
        Args:
            expected_url: String URL should contain
        
        Raises:
            AssertionError if URL doesn't match
        """
        logger.info(f"Asserting URL contains: {expected_url}")
        current_url = self.get_current_url()
        if expected_url not in current_url:
            error = f"Expected URL to contain '{expected_url}', got '{current_url}'"
            logger.error(error)
            raise AssertionError(error)

