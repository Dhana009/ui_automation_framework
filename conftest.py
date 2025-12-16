"""
Pytest configuration and fixtures.
This file is automatically discovered by pytest.
All fixtures defined here are available to all tests.
"""

import os
import pytest
from pathlib import Path

# Set environment for config loading
os.environ.setdefault("ENV", "dev")

print("\n" + "="*60)
print("🚀 UI Automation Framework - Initializing")
print(f"📍 Environment: {os.getenv('ENV', 'dev')}")
print("="*60 + "\n")

