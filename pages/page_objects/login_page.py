"""
Login Page Object

Example page object demonstrating BasePage inheritance and usage.
Contains selectors and methods specific to the login page.

All common interactions (click, type, wait, etc.) are inherited from BasePage.
"""

from pages.base_page import BasePage
from config.settings import config
from utils.logger import get_logger

logger = get_logger(__name__)


class LoginPage(BasePage):
    """
    Login page object.
    
    Demonstrates:
    - Inheriting from BasePage
    - Using BasePage methods
    - Page-specific methods
    - Using config system
    """
    
    # ==================== SELECTORS ====================
    
    # Input fields
    EMAIL_INPUT = "input[data-testid='email']"
    PASSWORD_INPUT = "input[data-testid='password']"
    
    # Buttons
    LOGIN_BUTTON = "button[data-testid='login-button']"
    REMEMBER_ME_CHECKBOX = "input[data-testid='remember-me']"
    
    # Messages
    ERROR_MESSAGE = ".error-message"
    SUCCESS_MESSAGE = ".success-message"
    
    # Page elements
    LOGIN_FORM = "form[data-testid='login-form']"
    PAGE_TITLE = "h1"
    
    # ==================== METHODS ====================
    
    def navigate_to_login(self):
        """
        Navigate to login page.
        Uses base_url from config.
        """
        logger.info("Navigating to login page")
        self.goto(config.base_url)
        self.wait_for_element_visible(self.LOGIN_FORM)
        logger.info("Login page loaded")
    
    def enter_email(self, email: str):
        """
        Enter email in email field.
        
        Args:
            email: Email address to enter
        """
        logger.info(f"Entering email: {email}")
        self.type_text(self.EMAIL_INPUT, email)
    
    def enter_password(self, password: str):
        """
        Enter password in password field.
        
        Args:
            password: Password to enter
        """
        logger.info("Entering password")
        self.type_text(self.PASSWORD_INPUT, password)
    
    def click_login_button(self):
        """Click login button."""
        logger.info("Clicking login button")
        self.click(self.LOGIN_BUTTON)
    
    def login(self, email: str, password: str):
        """
        Perform complete login flow.
        
        Args:
            email: Email address
            password: Password
        
        Example:
            login_page.login("user@example.com", "password123")
        """
        logger.info(f"Logging in as: {email}")
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()
        logger.info("Login button clicked, waiting for navigation...")
    
    def login_with_remember_me(self, email: str, password: str):
        """
        Login with "Remember Me" checkbox checked.
        
        Args:
            email: Email address
            password: Password
        """
        logger.info(f"Logging in with 'Remember Me': {email}")
        self.enter_email(email)
        self.enter_password(password)
        self.check_checkbox(self.REMEMBER_ME_CHECKBOX)
        self.click_login_button()
    
    # ==================== VERIFICATION METHODS ====================
    
    def verify_login_page_displayed(self):
        """
        Verify login page is displayed.
        
        Returns:
            True if login form is visible
        """
        logger.info("Verifying login page is displayed")
        self.assert_element_visible(self.LOGIN_FORM)
        return True
    
    def verify_error_message_displayed(self, expected_error: str = None):
        """
        Verify error message is displayed.
        
        Args:
            expected_error: Expected error message text
        
        Returns:
            Actual error message text
        """
        logger.info("Verifying error message displayed")
        self.assert_element_visible(self.ERROR_MESSAGE)
        
        error_text = self.get_text(self.ERROR_MESSAGE)
        
        if expected_error:
            self.assert_text_contains(self.ERROR_MESSAGE, expected_error)
            logger.info(f"Error message verified: {error_text}")
        
        return error_text
    
    def verify_no_error_message(self):
        """
        Verify error message is NOT displayed.
        
        Returns:
            True if error message not present
        """
        logger.info("Verifying no error message displayed")
        is_present = self.is_element_present(self.ERROR_MESSAGE)
        assert not is_present, "Error message should not be displayed"
        return True
    
    def get_login_page_title(self) -> str:
        """
        Get login page title.
        
        Returns:
            Page title text
        """
        title = self.get_text(self.PAGE_TITLE)
        logger.info(f"Login page title: {title}")
        return title
    
    def is_login_form_ready(self) -> bool:
        """
        Check if login form is ready for input.
        
        Returns:
            True if form is ready
        """
        logger.info("Checking if login form is ready")
        
        email_visible = self.is_visible(self.EMAIL_INPUT)
        password_visible = self.is_visible(self.PASSWORD_INPUT)
        button_enabled = self.is_enabled(self.LOGIN_BUTTON)
        
        ready = email_visible and password_visible and button_enabled
        logger.info(f"Login form ready: {ready}")
        
        return ready
    
    def wait_for_login_page_load(self):
        """
        Wait for login page to fully load.
        
        Waits for:
        - Form visible
        - Network idle
        - Page title visible
        """
        logger.info("Waiting for login page to load")
        self.wait_for_element_visible(self.LOGIN_FORM)
        self.wait_for_load_state("networkidle")
        self.wait_for_element_visible(self.PAGE_TITLE)
        logger.info("Login page fully loaded")

