import os
from typing import Any, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Represents the bot's configuration."""

    def __init__(self, config_file: Optional[str] = None):
        """Initializes the Config instance with configuration values.

        Args:
            config_file: The path to the configuration file. If None, uses environment variables.
        """
        self.config: Dict[str, Any] = {}
        self.config_file = config_file
        if config_file:
            self.load_from_file()
        else:
            self.load_from_env()

    def load_from_file(self):
        """Loads configuration values from a file."""
        try:
            with open(self.config_file, 'r') as f:
                self.config = eval(f.read())
        except FileNotFoundError:
            raise ConfigError(f"Configuration file '{self.config_file}' not found.")
        except Exception as e:
            raise ConfigError(f"Error loading configuration from file: {e}")

    def load_from_env(self):
        """Loads configuration values from environment variables."""
        self.config = {
            'token': os.getenv('DISCORD_TOKEN'),
            'prefix': os.getenv('PREFIX', '!'),
            'database_path': os.getenv('DATABASE_PATH', 'melody.db'),
            'youtube_api_key': os.getenv('YOUTUBE_API_KEY'),
            'spotify_client_id': os.getenv('SPOTIFY_CLIENT_ID'),
            'spotify_client_secret': os.getenv('SPOTIFY_CLIENT_SECRET'),
            'soundcloud_client_id': os.getenv('SOUNDCLOUD_CLIENT_ID'),
            'soundcloud_client_secret': os.getenv('SOUNDCLOUD_CLIENT_SECRET'),
        }

    def save(self):
        """Saves the configuration to a file."""
        try:
            with open(self.config_file, 'w') as f:
                f.write(str(self.config))
        except Exception as e:
            raise ConfigError(f"Error saving configuration to file: {e}")

    def get(self, key: str) -> Any:
        """Retrieves a configuration value."""
        return self.config.get(key)

    def set(self, key: str, value: Any):
        """Sets a configuration value."""
        self.config[key] = value

class ConfigError(Exception):
    """Custom exception class for configuration errors."""
    pass