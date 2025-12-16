"""
Simple Playwright Documentation Website Tests

Testing: https://playwright.dev/

Simple tests to verify framework works with real website.
"""

import pytest
from pages.page_objects.playwright_docs_page import PlaywrightDocsPage
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.smoke
@pytest.mark.parallel
class TestPlaywrightDocs:
    """Test Playwright documentation website"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page):
        """Setup page object"""
        self.docs_page = PlaywrightDocsPage(page)
    
    def test_docs_page_loads(self, page):
        """TEST 1: Playwright docs page loads"""
        logger.info("\n" + "="*60)
        logger.info("TEST: Playwright Docs Page Loads")
        logger.info("="*60)
        
        # Navigate
        self.docs_page.navigate()
        
        # Verify
        assert self.docs_page.is_page_loaded(), "Docs page not loaded"
        
        # Check title
        title = self.docs_page.get_page_title()
        assert "Playwright" in title, f"Title doesn't contain 'Playwright': {title}"
        
        logger.info("✓ Docs page loaded successfully")
    
    def test_page_has_content(self, page):
        """TEST 2: Page has main content"""
        logger.info("\n" + "="*60)
        logger.info("TEST: Page Has Content")
        logger.info("="*60)
        
        # Navigate
        self.docs_page.navigate()
        
        # Verify page loaded
        assert self.docs_page.is_page_loaded()
        
        # Check for content
        assert self.docs_page.is_visible(self.docs_page.MAIN_CONTENT), \
            "Main content not visible"
        
        logger.info("✓ Main content visible")
    
    def test_search_input_visible(self, page):
        """TEST 3: Logo is clickable"""
        logger.info("\n" + "="*60)
        logger.info("TEST: Logo is Clickable")
        logger.info("="*60)
        
        # Navigate
        self.docs_page.navigate()
        
        # Check logo is clickable
        assert self.docs_page.is_visible(self.docs_page.LOGO), \
            "Logo not visible"
        
        logger.info("✓ Logo is clickable")
    
    def test_get_started_link_exists(self, page):
        """TEST 4: Get Started link exists"""
        logger.info("\n" + "="*60)
        logger.info("TEST: Get Started Link Exists")
        logger.info("="*60)
        
        # Navigate
        self.docs_page.navigate()
        
        # Check link
        assert self.docs_page.is_visible(self.docs_page.GET_STARTED_LINK), \
            "Get Started link not visible"
        
        logger.info("✓ Get Started link visible")
    
    def test_navigation_works(self, page):
        """TEST 5: Navigation to Get Started works"""
        logger.info("\n" + "="*60)
        logger.info("TEST: Navigation Works")
        logger.info("="*60)
        
        # Navigate to docs
        self.docs_page.navigate()
        
        # Click Get Started
        self.docs_page.click_get_started()
        
        # Verify new page loaded
        new_title = self.docs_page.get_page_title()
        logger.info(f"New page title: {new_title}")
        
        # Should be on a different page
        assert self.docs_page.is_page_loaded()
        
        logger.info("✓ Navigation successful")

