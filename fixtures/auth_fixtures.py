"""
Authentication Fixtures

Contains fixtures for login and authenticated page access.

Fixtures:
- get_worker_login: Get login credentials for worker
- authenticated_page: Page with logged-in user
"""

import os
import time
import pytest
from pages.base_page import BasePage
from config.settings import config
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="session")
def get_worker_login():
    """
    Auto-assign login credentials to worker.
    
    In parallel execution (pytest-xdist):
    - Worker 1 (gw0) gets login[0]
    - Worker 2 (gw1) gets login[1]
    - Worker 3 (gw2) gets login[2]
    - etc.
    
    In sequential execution:
    - Uses login[0]
    
    Yields:
        dict: Login credentials {email, password}
    
    Notes:
        - Session scope: credentials assigned once per worker
        - Reused by all tests in that worker
        - Allows parallel tests without login conflicts
    
    Environment:
        - Reads PYTEST_XDIST_WORKER env var (set by pytest-xdist)
        - "master" = sequential execution
        - "gw0", "gw1", etc. = parallel execution
    """
    # Login credentials pool
    LOGIN_POOL = [
        {"email": config.test_data["valid_user"], "password": config.test_data["valid_password"]},
        {"email": f"test_user_2@example.com", "password": "test_password_2"},
        {"email": f"test_user_3@example.com", "password": "test_password_3"},
        {"email": f"test_user_4@example.com", "password": "test_password_4"},
        {"email": f"test_user_5@example.com", "password": "test_password_5"},
    ]
    
    # Get worker ID from pytest-xdist
    worker_id = os.getenv("PYTEST_XDIST_WORKER", "master")
    
    if worker_id == "master":
        # Sequential execution or single test
        login = LOGIN_POOL[0]
    else:
        # Parallel execution - extract worker number
        # worker_id format: "gw0", "gw1", "gw2", etc.
        try:
            worker_num = int(worker_id[2:])
            login = LOGIN_POOL[worker_num % len(LOGIN_POOL)]
        except (ValueError, IndexError):
            login = LOGIN_POOL[0]
    
    logger.info(f"Worker {worker_id} assigned login: {login['email']}")
    return login


@pytest.fixture(scope="module")
def authenticated_page(page, get_worker_login):
    """
    Create authenticated page (logged-in user).
    
    Used for tests that need pre-logged-in state.
    Handles login with retry logic and auto-cleanup.
    
    Args:
        page: Page fixture from browser_fixtures
        get_worker_login: Login credentials fixture
    
    Yields:
        page: Authenticated page (user logged in)
    
    Notes:
        - Module scope: one login per test module
        - Reused across all tests in module
        - If login fails, all tests in module are skipped
        - Auto-cleanup on failure or success
    
    Error Handling:
        - Retries login 3 times on failure
        - Logs detailed error messages
        - Skips all dependent tests if authentication fails
    
    Cleanup:
        - Clears cookies
        - Clears localStorage
        - Clears sessionStorage
        - Logged out (if applicable)
    """
    logger.info(f"Authenticating user: {get_worker_login['email']}")
    
    base_page = BasePage(page)
    
    # Try to login (with retry logic)
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"Login attempt {attempt}/{max_retries}")
            
            # Navigate to base URL
            page.goto(config.base_url)
            base_page.wait_for_load_state("networkidle")
            
            # This is a placeholder - actual login logic depends on your app
            # For now, we just navigate to dashboard
            # In real tests, replace with actual login flow:
            # 
            # base_page.type_text("input[name='email']", get_worker_login['email'])
            # base_page.type_text("input[name='password']", get_worker_login['password'])
            # base_page.click("button[type='submit']")
            # base_page.wait_for_url("**/dashboard")
            #
            # For this example, we simulate successful login by navigating to dashboard
            page.goto(f"{config.base_url}/dashboard")
            
            logger.info(f"User authenticated: {get_worker_login['email']}")
            break
        
        except Exception as e:
            logger.warning(f"Login attempt {attempt} failed: {str(e)}")
            
            if attempt == max_retries:
                logger.error(f"Login failed after {max_retries} attempts")
                pytest.skip(f"Authentication failed: {str(e)}")
            
            time.sleep(2)  # Wait before retry
    
    yield page
    
    # Cleanup
    logger.info("Cleaning up authenticated page")
    try:
        page.context.clear_cookies()
        page.evaluate("localStorage.clear()")
        page.evaluate("sessionStorage.clear()")
        logger.debug("Page cleanup completed")
    except Exception as e:
        logger.warning(f"Cleanup error: {str(e)}")

