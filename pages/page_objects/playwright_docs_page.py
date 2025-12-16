"""
Playwright Documentation Website Page Object

Simple page object for testing https://playwright.dev/
"""

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class PlaywrightDocsPage(BasePage):
    """Playwright documentation page"""
    
    # Selectors
    LOGO = "a.navbar__brand"
    SEARCH_INPUT = "input[class*='search']"
    GET_STARTED_LINK = "a:has-text('Get started')"
    INSTALLATION_HEADER = "h1"
    MAIN_CONTENT = "main"
    
    def __init__(self, page):
        super().__init__(page)
        logger.info("Initialized PlaywrightDocsPage")
    
    def navigate(self):
        """Navigate to Playwright docs"""
        logger.info("Navigating to Playwright docs")
        self.goto("https://playwright.dev/")
        self.wait_for_load_state("networkidle")
        logger.info("Playwright docs loaded")
    
    def is_page_loaded(self) -> bool:
        """Check if page loaded"""
        logger.info("Checking if Playwright docs loaded")
        try:
            is_visible = self.is_visible(self.LOGO)
            logger.info(f"Page loaded: {is_visible}")
            return is_visible
        except:
            return False
    
    def get_page_title(self) -> str:
        """Get page title"""
        title = self.page.title()
        logger.info(f"Page title: {title}")
        return title
    
    def click_get_started(self):
        """Click Get Started link"""
        logger.info("Clicking Get Started")
        self.click(self.GET_STARTED_LINK)
        self.wait_for_load_state("networkidle")
        logger.info("Get Started page loaded")

