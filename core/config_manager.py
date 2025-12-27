import json
import os

class ConfigManager:
    _config = None  # class-level cache

    @classmethod
    def load(cls, config_path="config.json"):
        if cls._config is None:
            if not os.path.exists(config_path):
                raise FileNotFoundError(f"{config_path} not found")

            with open(config_path, "r") as f:
                cls._config = json.load(f)

        return cls._config

    @classmethod
    def get(cls, key, default=None):
        if cls._config is None:
            cls.load()
        return cls._config.get(key, default)
