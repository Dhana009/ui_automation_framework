"""
Pytest Configuration and Hooks

This file is automatically discovered by pytest.

Imports fixtures from:
- fixtures.browser_fixtures: browser, page, playwright_instance
- fixtures.auth_fixtures: get_worker_login, authenticated_page

Defines hooks:
- pytest_runtest_makereport: Screenshot on failure
- pytest_configure: Setup before tests
- pytest_sessionstart: Setup at session start
- pytest_sessionfinish: Cleanup after session
"""

import os
import time
import pytest
from pathlib import Path

from config.settings import config
from utils.logger import get_logger

# Import all fixtures from fixtures modules
# This makes them available to all tests
from fixtures.browser_fixtures import playwright_instance, browser, page
from fixtures.auth_fixtures import get_worker_login, authenticated_page
from fixtures.database_fixtures import setup_test_database, test_db, reset_test_data
from fixtures.server_fixtures import start_test_server, api_server, server_health

logger = get_logger(__name__)

# Set environment for config loading
os.environ.setdefault("ENV", "dev")

print("\n" + "="*60)
print("UI Automation Framework - Initializing")
print(f"Environment: {os.getenv('ENV', 'dev')}")
print("="*60 + "\n")


# ==================== PYTEST HOOKS ====================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture screenshot on test failure.
    
    Args:
        item: Test item
        call: Call info
    """
    yield
    
    # Only capture on failure
    if call.excinfo is not None:
        # Try to get page fixture
        if "page" in item.fixturenames:
            try:
                page = item.funcargs.get("page")
                if page:
                    # Take screenshot
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    screenshots_dir = Path(__file__).parent / "screenshots"
                    screenshots_dir.mkdir(exist_ok=True)
                    
                    screenshot_path = screenshots_dir / f"{item.name}_{timestamp}_FAILED.png"
                    page.screenshot(path=str(screenshot_path))
                    logger.error(f"Screenshot saved on failure: {screenshot_path}")
            except Exception as e:
                logger.warning(f"Failed to capture screenshot: {str(e)}")


def pytest_configure(config):
    """
    Pytest configuration hook (runs before tests).
    
    Args:
        config: Pytest config
    """
    logger.info("Pytest configuration started")
    
    # Create necessary directories
    screenshots_dir = Path(__file__).parent / "screenshots"
    logs_dir = Path(__file__).parent / "logs"
    reports_dir = Path(__file__).parent / "reports"
    
    screenshots_dir.mkdir(exist_ok=True)
    logs_dir.mkdir(exist_ok=True)
    reports_dir.mkdir(exist_ok=True)
    
    logger.info("Directories created/verified")


def pytest_sessionstart(session):
    """
    Pytest hook that runs at session start.
    
    Args:
        session: Pytest session
    """
    logger.info("="*60)
    logger.info("TEST SESSION STARTED")
    logger.info(f"Environment: {config.env}")
    logger.info(f"Base URL: {config.base_url}")
    logger.info("="*60)


def pytest_sessionfinish(session, exitstatus):
    """
    Pytest hook that runs at session end.
    
    Args:
        session: Pytest session
        exitstatus: Test exit status
    """
    logger.info("="*60)
    status = "PASSED" if exitstatus == 0 else "FAILED"
    logger.info(f"TEST SESSION FINISHED - {status}")
    logger.info("="*60)

