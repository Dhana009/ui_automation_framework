"""
Login Test Suite

Demonstrates:
- Using page objects (LoginPage, DashboardPage)
- Using fixtures (page, authenticated_page)
- Using config system
- Using markers (smoke, parallel)
- Using assertions from BasePage
- Logging and screenshots
"""

import pytest
from pages.page_objects.login_page import LoginPage
from pages.page_objects.dashboard_page import DashboardPage
from config.settings import config


@pytest.mark.smoke
@pytest.mark.parallel
class TestLoginFlow:
    """Login flow test suite."""
    
    def test_login_page_loads_successfully(self, page):
        """
        Test that login page loads successfully.
        
        Demonstrates:
        - Using 'page' fixture
        - Navigating to URL from config
        - Page object initialization
        - BasePage methods
        """
        # Arrange
        login_page = LoginPage(page)
        
        # Act
        login_page.navigate_to_login()
        
        # Assert
        login_page.verify_login_page_displayed()
        assert login_page.is_login_form_ready()
    
    def test_valid_login_redirects_to_dashboard(self, page):
        """
        Test successful login with valid credentials.
        
        Demonstrates:
        - Multi-step page interactions
        - Using config.test_data for credentials
        - URL wait verification
        - Page transitions
        """
        # Arrange
        login_page = LoginPage(page)
        dashboard_page = DashboardPage(page)
        
        # Act
        login_page.navigate_to_login()
        login_page.login(
            config.test_data["valid_user"],
            config.test_data["valid_password"]
        )
        
        # Wait for navigation to dashboard
        page.wait_for_url("**/dashboard", timeout=config.timeouts["page_load"] * 1000)
        
        # Assert
        dashboard_page.verify_dashboard_loaded()
        assert "Welcome" in dashboard_page.get_welcome_message()
    
    def test_invalid_credentials_shows_error(self, page):
        """
        Test login with invalid credentials shows error.
        
        Demonstrates:
        - Error state verification
        - Custom assertions
        - Text validation
        """
        # Arrange
        login_page = LoginPage(page)
        
        # Act
        login_page.navigate_to_login()
        login_page.login("invalid@example.com", "wrongpassword")
        
        # Assert - error should be visible (waiting for page to process)
        page.wait_for_timeout(2000)  # Give page time to show error
        
        login_page.verify_error_message_displayed()
        # Still on login page
        login_page.verify_login_page_displayed()
    
    def test_login_with_remember_me(self, page):
        """
        Test login with "Remember Me" checkbox.
        
        Demonstrates:
        - Checkbox interactions
        - Multi-step form filling
        - Form element state checks
        """
        # Arrange
        login_page = LoginPage(page)
        
        # Act
        login_page.navigate_to_login()
        login_page.login_with_remember_me(
            config.test_data["valid_user"],
            config.test_data["valid_password"]
        )
        
        # Wait for navigation
        page.wait_for_url("**/dashboard", timeout=config.timeouts["page_load"] * 1000)
        
        # Assert
        assert page.url.endswith("/dashboard")


@pytest.mark.smoke
@pytest.mark.parallel
class TestDashboardAfterLogin:
    """Dashboard verification tests after login."""
    
    def test_dashboard_displays_user_info(self, authenticated_page):
        """
        Test dashboard displays logged-in user info.
        
        Demonstrates:
        - Using authenticated_page fixture (pre-logged-in)
        - Text extraction
        - Element verification
        """
        # Arrange
        dashboard_page = DashboardPage(authenticated_page)
        
        # Act
        dashboard_page.wait_for_loading_spinner_to_disappear()
        username = dashboard_page.get_logged_in_username()
        email = dashboard_page.get_logged_in_email()
        
        # Assert
        dashboard_page.verify_dashboard_loaded()
        dashboard_page.verify_user_is_logged_in()
        assert username is not None
        assert email is not None
    
    def test_dashboard_has_all_elements(self, authenticated_page):
        """
        Test dashboard has all required elements.
        
        Demonstrates:
        - Multiple element verification
        - Custom verification methods
        - Comprehensive assertions
        """
        # Arrange
        dashboard_page = DashboardPage(authenticated_page)
        
        # Act & Assert
        dashboard_page.verify_dashboard_elements()
        
        # Additional verification
        welcome_msg = dashboard_page.get_welcome_message()
        assert welcome_msg is not None
        assert len(welcome_msg) > 0
    
    def test_logout_redirects_to_login(self, authenticated_page):
        """
        Test logout functionality.
        
        Demonstrates:
        - Click action
        - Navigation wait
        - URL verification
        """
        # Arrange
        dashboard_page = DashboardPage(authenticated_page)
        login_page = LoginPage(authenticated_page)
        
        # Act
        dashboard_page.logout()
        dashboard_page.wait_for_logout_redirect()
        
        # Assert
        login_page.verify_login_page_displayed()
        assert "login" in authenticated_page.url.lower()


@pytest.mark.smoke
@pytest.mark.parallel
def test_page_objects_inherit_basepage_methods(page):
    """
    Test that page objects have access to all BasePage methods.
    
    Demonstrates:
    - Inheritance verification
    - Method availability
    - BasePage method usage
    """
    # Arrange
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)
    
    # Act & Assert - verify BasePage methods are available
    
    # From BasePage
    assert hasattr(login_page, 'click')
    assert hasattr(login_page, 'type_text')
    assert hasattr(login_page, 'wait_for_element')
    assert hasattr(login_page, 'is_visible')
    assert hasattr(login_page, 'get_text')
    
    # Assertions from BasePage
    assert hasattr(login_page, 'assert_element_visible')
    assert hasattr(login_page, 'assert_text_contains')
    assert hasattr(login_page, 'assert_page_title')
    
    # Verify for dashboard_page too
    assert hasattr(dashboard_page, 'click')
    assert hasattr(dashboard_page, 'scroll_to_element')
    assert hasattr(dashboard_page, 'take_screenshot')
    
    print("All BasePage methods are available to page objects")


@pytest.mark.smoke
@pytest.mark.parallel
def test_config_system_works(page):
    """
    Test that config system is working correctly.
    
    Demonstrates:
    - Config access in tests
    - Environment-based config
    - Config values availability
    """
    # Assert config is loaded
    assert config.base_url is not None
    assert config.browser_config is not None
    assert config.timeouts is not None
    assert config.test_data is not None
    
    # Verify specific config values
    assert "http" in config.base_url or "https" in config.base_url
    assert config.timeouts["element_wait"] > 0
    assert config.timeouts["page_load"] > 0
    
    # Verify test data
    assert config.test_data["valid_user"] is not None
    assert config.test_data["valid_password"] is not None
    
    print(f"Config loaded successfully for environment: {config.env}")
    print(f"Base URL: {config.base_url}")
    print(f"Browser: {config.browser_config['name']}")

