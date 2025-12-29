import os

class ConfigManager:
    @staticmethod
    def get(key, default=None):
        """Get a config value from environment variables."""
        return os.environ.get(key, default)
