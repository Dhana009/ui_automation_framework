"""
Configuration Manager

Loads environment-specific settings from YAML files.
Provides centralized access to configuration throughout the framework.

Usage:
    from config.settings import config
    
    config.base_url              # Get base URL
    config.browser_config        # Get browser configuration
    config.timeouts              # Get timeout settings
    config.test_data             # Get test data (credentials, etc.)
    config.logging               # Get logging settings
"""

import os
import yaml
from pathlib import Path


class Config:
    """Configuration loader that reads YAML files based on environment."""
    
    def __init__(self, env: str = None):
        """
        Initialize configuration from YAML file.
        
        Args:
            env: Environment name (dev, qa, prod). If None, reads from ENV variable.
                 Defaults to 'dev' if neither is provided.
        
        Raises:
            FileNotFoundError: If config file for environment doesn't exist.
        """
        self.env = env or os.getenv("ENV", "dev")
        self.config_file = Path(__file__).parent / "env" / f"{self.env}.yaml"
        
        if not self.config_file.exists():
            raise FileNotFoundError(
                f"Config file not found: {self.config_file}\n"
                f"   Available environments: dev, qa, prod"
            )
        
        with open(self.config_file, "r") as f:
            self.config = yaml.safe_load(f)
    
    @property
    def base_url(self) -> str:
        """Get base URL for testing."""
        return self.config["base_url"]
    
    @property
    def browser_config(self) -> dict:
        """Get browser configuration (name, headless, viewport, etc.)."""
        return self.config["browser"]
    
    @property
    def timeouts(self) -> dict:
        """Get timeout settings (page_load, element_wait, network)."""
        return self.config["timeouts"]
    
    @property
    def test_data(self) -> dict:
        """Get test data (credentials, test users, etc.)."""
        return self.config["test_data"]
    
    @property
    def logging(self) -> dict:
        """Get logging configuration (level, to_file, etc.)."""
        return self.config["logging"]
    
    @property
    def screenshots(self) -> dict:
        """Get screenshot configuration."""
        return self.config.get("screenshots", {})
    
    def get(self, key: str, default=None):
        """
        Get any configuration value by key.
        
        Args:
            key: Configuration key to retrieve.
            default: Default value if key doesn't exist.
        
        Returns:
            Configuration value or default.
        """
        return self.config.get(key, default)
    
    def __repr__(self) -> str:
        """String representation of config object."""
        return f"Config(env='{self.env}', base_url='{self.base_url}')"


# Global configuration instance - loaded once at startup
# This instance is used throughout the framework
config = Config() # Global configuration instance 
#why? because we want to use the same configuration instance throughout the framework so that we don't have to load the configuration file multiple times.