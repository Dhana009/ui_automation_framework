"""
Constants

Framework-wide constants and defaults.
"""

# Timeout constants (in seconds)
DEFAULT_TIMEOUT = 10
PAGE_LOAD_TIMEOUT = 30
NETWORK_TIMEOUT = 20

# Retry settings
DEFAULT_RETRY_ATTEMPTS = 3
DEFAULT_RETRY_DELAY = 2

# Viewport sizes
DESKTOP_VIEWPORT = {"width": 1280, "height": 720}
MOBILE_VIEWPORT = {"width": 375, "height": 667}
TABLET_VIEWPORT = {"width": 768, "height": 1024}

# Error messages
ELEMENT_NOT_FOUND = "Element not found: {}"
ELEMENT_NOT_VISIBLE = "Element not visible: {}"
TIMEOUT_ERROR = "Operation timed out after {} seconds"

