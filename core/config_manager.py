import os

class ConfigManager:
    """
    Configuration manager that reads from environment variables only.
    No config.json file needed.
    """
    
    @staticmethod
    def get(key, default=None):
        """
        Get a config value from environment variables.
        
        Args:
            key: The environment variable name
            default: Default value if not found
            
        Returns:
            The environment variable value or default
        """
        return os.environ.get(key, default)

