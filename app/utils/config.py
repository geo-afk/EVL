import os
from typing import Optional, Any
from dotenv import load_dotenv

class Config:
    """
    Load configuration values from environment variables (and a .env file) and expose as attributes.
    """

    def __init__(self,
                 env_file: Optional[str] = None,
                 **defaults: Any):
        """
        :param env_file: optional path to a .env file to load
        :param defaults: dict of default values for various config keys
        """
        # Load .env file if provided (or default to just load .env in working dir)
        if env_file:
            load_dotenv(dotenv_path=env_file, override=False)
        else:
            load_dotenv(override=False)

        # Store defaults
        self._defaults = defaults

        # Populate attributes
        for key, default in defaults.items():
            # Use os.getenv so environment > .env file > default
            value = os.getenv(key, default)
            setattr(self, key, value)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a config value (first environment, then defaults)."""
        return os.getenv(key, getattr(self, key, default))

    def as_dict(self) -> dict:
        """Return all config keys + values as dict."""
        return {key: getattr(self, key) for key in self._defaults.keys()}
