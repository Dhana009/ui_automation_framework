"""
Browser Fixtures

Contains browser and page initialization fixtures.
Used for all tests that need browser access.

Fixtures:
- playwright_instance: Playwright instance (session scope)
- browser: Browser instance (function scope)
- page: Page instance (function scope)
"""

import pytest
from playwright.sync_api import sync_playwright
from config.settings import config
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="session")
def playwright_instance():
    """
    Initialize Playwright instance (once per test session).
    
    Yields:
        playwright: Playwright instance
    
    Notes:
        - Session scope: created once, shared by all tests
        - All browsers created from this instance
        - Closed after all tests complete
    """
    logger.info("Starting Playwright instance")
    playwright = sync_playwright().start()
    yield playwright
    logger.info("Stopping Playwright instance")
    playwright.stop()


@pytest.fixture(scope="function")
def browser(playwright_instance):
    """
    Create new browser instance (new for each test).
    Uses browser configuration from config system.
    
    Args:
        playwright_instance: Playwright instance from session fixture
    
    Yields:
        browser: Playwright browser instance
    
    Notes:
        - Function scope: new browser per test
        - Automatically closed after test
        - Uses settings from config/env/{ENV}.yaml
    
    Config Used:
        - browser.name: "chromium", "firefox", or "webkit"
        - browser.headless: true/false
        - browser.slow_mo: milliseconds for slow motion
    """
    logger.info("Launching browser")
    
    browser_config = config.browser_config
    browser_type = getattr(playwright_instance, browser_config["name"])
    
    browser = browser_type.launch(
        headless=browser_config.get("headless", True),
        slow_mo=browser_config.get("slow_mo", 0)
    )
    
    logger.debug(f"Browser launched: {browser_config['name']}")
    yield browser
    
    logger.info("Closing browser")
    browser.close()


@pytest.fixture(scope="function")
def page(browser):
    """
    Create new page in browser (new for each test).
    Sets default timeouts from config.
    
    Args:
        browser: Browser instance from browser fixture
    
    Yields:
        page: Playwright page instance
    
    Notes:
        - Function scope: new page per test
        - Page inherits browser context
        - Timeouts set from config system
        - Automatically closed after test
    
    Config Used:
        - browser.viewport: {width, height}
        - timeouts.element_wait: for selector waits
        - timeouts.page_load: for navigation waits
    """
    logger.info("Creating new page")
    
    viewport = config.browser_config.get("viewport")
    page = browser.new_page(viewport=viewport) if viewport else browser.new_page()
    
    # Set default timeouts from config
    page.set_default_timeout(config.timeouts["element_wait"] * 1000)
    page.set_default_navigation_timeout(config.timeouts["page_load"] * 1000)
    
    logger.debug(f"Page created with viewport: {viewport}")
    yield page
    
    logger.info("Closing page")
    page.close()

