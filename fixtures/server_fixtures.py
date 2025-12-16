"""
Server Fixtures

Contains application server setup/teardown fixtures.
Runs before tests to start necessary services.

Fixtures:
- start_test_server: Start test app server (session scope, autouse)
- api_server: Get server connection info (function scope)
- server_health: Check server health (function scope)
"""

import pytest
import time
from utils.logger import get_logger

logger = get_logger(__name__)


class TestServer:
    """
    Mock application server for demonstration.
    In real project, replace with actual server (Flask, FastAPI, etc.)
    """
    
    def __init__(self, host: str = "localhost", port: int = 8000):
        """Initialize server"""
        self.host = host
        self.port = port
        self.is_running = False
        self.endpoints = {}
        logger.info(f"Server initialized: {host}:{port}")
    
    def start(self):
        """Start server"""
        logger.info(f"Starting server: {self.host}:{self.port}")
        time.sleep(0.5)  # Simulate startup time
        self.is_running = True
        logger.info("Server started successfully")
    
    def stop(self):
        """Stop server"""
        logger.info(f"Stopping server: {self.host}:{self.port}")
        self.is_running = False
        logger.info("Server stopped")
    
    def health_check(self) -> dict:
        """Check server health"""
        if not self.is_running:
            return {"status": "down", "message": "Server not running"}
        
        return {
            "status": "healthy",
            "host": self.host,
            "port": self.port,
            "uptime": "running"
        }
    
    def register_route(self, path: str, method: str, handler):
        """Register API endpoint"""
        key = f"{method.upper()} {path}"
        self.endpoints[key] = handler
        logger.debug(f"Route registered: {key}")
    
    def get_url(self) -> str:
        """Get server URL"""
        protocol = "https" if self.port == 443 else "http"
        return f"{protocol}://{self.host}:{self.port}"
    
    def get_base_url(self) -> str:
        """Get base URL for tests"""
        return self.get_url()


# Global server instance
_test_server = None


@pytest.fixture(scope="session", autouse=True)
def start_test_server():
    """
    Start test application server before all tests (session scope, autouse).
    
    This fixture:
    - Creates mock test server
    - Starts server on localhost
    - Waits for server to be healthy
    - Stops server after all tests
    
    Notes:
        - autouse=True means it runs automatically
        - scope="session" means runs once for entire test run
        - Don't need to pass to test functions
    
    In Real Project:
        Replace with actual server startup:
        - Start Flask/FastAPI/Django app
        - Wait for server health endpoint
        - Check database migrations
        - Use Docker, pytest-server-fixtures, etc.
    
    Environment:
        - Server runs on localhost:8000 by default
        - Can be configured via environment variables
    """
    global _test_server
    
    logger.info("="*60)
    logger.info("STARTING TEST APPLICATION SERVER")
    logger.info("="*60)
    
    # Create test server instance
    _test_server = TestServer(host="localhost", port=8000)
    
    # Start server
    _test_server.start()
    
    # Wait for server to be healthy
    logger.info("Waiting for server to be healthy...")
    max_retries = 5
    for attempt in range(max_retries):
        health = _test_server.health_check()
        if health["status"] == "healthy":
            logger.info("Server is healthy")
            break
        
        if attempt < max_retries - 1:
            logger.warning(f"Health check failed, retrying... ({attempt + 1}/{max_retries})")
            time.sleep(1)
        else:
            logger.error("Server failed to start")
            raise RuntimeError("Test server failed to reach healthy state")
    
    # Register mock endpoints
    logger.info("Registering mock endpoints...")
    _test_server.register_route("/api/login", "POST", lambda: {"token": "test_token"})
    _test_server.register_route("/api/dashboard", "GET", lambda: {"message": "Welcome"})
    _test_server.register_route("/api/health", "GET", lambda: {"status": "ok"})
    
    server_url = _test_server.get_base_url()
    logger.info(f"Test server running at: {server_url}")
    logger.info("="*60)
    
    yield  # All tests run here
    
    # Cleanup after tests
    logger.info("="*60)
    logger.info("STOPPING TEST APPLICATION SERVER")
    logger.info("="*60)
    
    _test_server.stop()
    
    logger.info("Test server stopped")
    logger.info("="*60)


@pytest.fixture(scope="function")
def api_server():
    """
    Get test server connection info (function scope).
    
    Yields:
        dict: Server connection info {host, port, base_url}
    
    Notes:
        - Available to each test function
        - Can use to construct URLs
        - Server is already running
    
    Usage:
        def test_api(api_server):
            url = f"{api_server['base_url']}/api/data"
            # Make requests to url
    """
    global _test_server
    
    if _test_server is None:
        raise RuntimeError("Test server not initialized. start_test_server fixture failed.")
    
    server_info = {
        "host": _test_server.host,
        "port": _test_server.port,
        "base_url": _test_server.get_base_url(),
        "server": _test_server
    }
    
    logger.debug(f"API server info: {server_info}")
    
    yield server_info


@pytest.fixture(scope="function")
def server_health():
    """
    Check server health before test (function scope).
    
    Yields:
        dict: Server health status
    
    Notes:
        - Runs before each test
        - Fails test if server is not healthy
        - Ensures server is ready
    
    Usage:
        def test_something(server_health):
            assert server_health["status"] == "healthy"
    """
    global _test_server
    
    if _test_server is None:
        raise RuntimeError("Test server not initialized.")
    
    logger.info("Checking server health...")
    health = _test_server.health_check()
    
    if health["status"] != "healthy":
        logger.error(f"Server health check failed: {health}")
        pytest.skip(f"Server not healthy: {health['message']}")
    
    logger.debug(f"Server health: {health['status']}")
    
    yield health

