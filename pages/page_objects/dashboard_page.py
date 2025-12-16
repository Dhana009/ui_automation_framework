"""
Dashboard Page Object

Example page object demonstrating BasePage inheritance.
Contains selectors and methods specific to the dashboard page.
"""

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class DashboardPage(BasePage):
    """
    Dashboard page object.
    
    Demonstrates:
    - Inheriting from BasePage
    - Using various BasePage methods
    - Page-specific logic
    """
    
    # ==================== SELECTORS ====================
    
    # Main elements
    DASHBOARD_CONTAINER = "div[data-testid='dashboard']"
    WELCOME_MESSAGE = "h1[data-testid='welcome-message']"
    USER_INFO = "div[data-testid='user-info']"
    
    # Navigation
    SIDEBAR = "nav[data-testid='sidebar']"
    LOGOUT_BUTTON = "button[data-testid='logout-button']"
    PROFILE_BUTTON = "button[data-testid='profile-button']"
    
    # Content areas
    MAIN_CONTENT = "main[data-testid='main-content']"
    USER_NAME = "span[data-testid='user-name']"
    USER_EMAIL = "span[data-testid='user-email']"
    
    # Status elements
    STATUS_MESSAGE = "div[data-testid='status-message']"
    LOADING_SPINNER = "div[data-testid='loading']"
    
    # ==================== METHODS ====================
    
    def verify_dashboard_loaded(self):
        """
        Verify dashboard page is fully loaded.
        
        Checks:
        - Dashboard container visible
        - Welcome message visible
        - Network idle
        
        Returns:
            True if dashboard loaded
        """
        logger.info("Verifying dashboard is loaded")
        self.assert_element_visible(self.DASHBOARD_CONTAINER)
        self.assert_element_visible(self.WELCOME_MESSAGE)
        self.wait_for_load_state("networkidle")
        logger.info("Dashboard verified as loaded")
        return True
    
    def get_welcome_message(self) -> str:
        """
        Get welcome message text.
        
        Returns:
            Welcome message text
        """
        logger.info("Getting welcome message")
        message = self.get_text(self.WELCOME_MESSAGE)
        logger.info(f"Welcome message: {message}")
        return message
    
    def verify_user_is_logged_in(self, expected_username: str = None) -> bool:
        """
        Verify user is logged in.
        
        Args:
            expected_username: Expected username (optional)
        
        Returns:
            True if user is logged in
        """
        logger.info("Verifying user is logged in")
        self.assert_element_visible(self.USER_INFO)
        self.assert_element_visible(self.LOGOUT_BUTTON)
        
        if expected_username:
            actual_name = self.get_text(self.USER_NAME)
            self.assert_text_exact(self.USER_NAME, expected_username)
            logger.info(f"User verified: {actual_name}")
        
        logger.info("User is logged in")
        return True
    
    def get_logged_in_username(self) -> str:
        """
        Get currently logged-in username.
        
        Returns:
            Username text
        """
        logger.info("Getting logged-in username")
        username = self.get_text(self.USER_NAME)
        logger.info(f"Logged-in username: {username}")
        return username
    
    def get_logged_in_email(self) -> str:
        """
        Get currently logged-in user email.
        
        Returns:
            Email text
        """
        logger.info("Getting logged-in email")
        email = self.get_text(self.USER_EMAIL)
        logger.info(f"Logged-in email: {email}")
        return email
    
    def logout(self):
        """
        Click logout button to logout.
        
        After logout, user is redirected to login page.
        """
        logger.info("Clicking logout button")
        self.click(self.LOGOUT_BUTTON)
        logger.info("Logout button clicked")
    
    def wait_for_logout_redirect(self):
        """
        Wait for redirect to login page after logout.
        """
        logger.info("Waiting for redirect to login page")
        self.wait_for_url("**/login")
        logger.info("Redirected to login page")
    
    def click_profile_button(self):
        """Click profile button."""
        logger.info("Clicking profile button")
        self.click(self.PROFILE_BUTTON)
    
    def wait_for_loading_spinner_to_disappear(self):
        """
        Wait for loading spinner to disappear.
        
        Useful when waiting for async operations.
        """
        logger.info("Waiting for loading spinner to disappear")
        self.wait_for_element_hidden(self.LOADING_SPINNER)
        logger.info("Loading completed")
    
    def get_status_message(self) -> str:
        """
        Get status message displayed on dashboard.
        
        Returns:
            Status message text
        """
        logger.info("Getting status message")
        message = self.get_text(self.STATUS_MESSAGE)
        logger.info(f"Status message: {message}")
        return message
    
    def verify_dashboard_elements(self):
        """
        Verify all key dashboard elements are visible.
        
        Checks:
        - Dashboard container
        - Welcome message
        - Sidebar
        - User info
        - Main content
        - Logout button
        
        Returns:
            True if all elements visible
        """
        logger.info("Verifying all dashboard elements")
        
        self.assert_element_visible(self.DASHBOARD_CONTAINER)
        self.assert_element_visible(self.WELCOME_MESSAGE)
        self.assert_element_visible(self.SIDEBAR)
        self.assert_element_visible(self.USER_INFO)
        self.assert_element_visible(self.MAIN_CONTENT)
        self.assert_element_visible(self.LOGOUT_BUTTON)
        
        logger.info("All dashboard elements verified")
        return True
    
    def scroll_to_profile_section(self):
        """Scroll to profile section on page."""
        logger.info("Scrolling to profile section")
        self.scroll_to_element(self.USER_INFO)
    
    def take_dashboard_screenshot(self, name: str = "dashboard"):
        """
        Take screenshot of dashboard.
        
        Args:
            name: Screenshot name
        
        Returns:
            Path to screenshot
        """
        logger.info(f"Taking dashboard screenshot: {name}")
        path = self.take_screenshot(f"{name}.png")
        return path

