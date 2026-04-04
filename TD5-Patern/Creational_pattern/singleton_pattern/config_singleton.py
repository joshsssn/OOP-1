"""
Singleton Pattern - Configuration Manager
==========================================
Refactored from repeated load_config() calls
into a Singleton that loads the file ONCE and
shares the same instance across all services.
"""

import json


# ─────────────────────────────────────────────
# 1. The Singleton
# ─────────────────────────────────────────────

class ConfigManager:
    """
    Singleton configuration manager.
    - Loads config.json ONCE on first access
    - Returns the same instance on every subsequent call
    - Provides dot-notation access: get("database.host")
    """

    _instance = None  # Class-level: holds the single instance

    def __init__(self, config_path: str = "config.json"):
        """
        Private-by-convention constructor.
        Should not be called directly — use get_instance().
        """
        self._config_path = config_path
        self._config = self._load_file()
        print(f"[ConfigManager] Config loaded from '{config_path}' (this should appear ONCE)")

    def _load_file(self) -> dict:
        """Read and parse the JSON config file."""
        with open(self._config_path, "r") as f:
            return json.load(f)

    @classmethod
    def get_instance(cls, config_path: str = "config.json") -> "ConfigManager":
        """
        The Singleton access point.
        Creates the instance on first call, returns it on all others.
        """
        if cls._instance is None:
            cls._instance = ConfigManager(config_path)
        return cls._instance

    def get(self, key: str):
        """
        Access nested config values using dot notation.
        Example: get("database.host") → "localhost"
        """
        keys = key.split(".")
        value = self._config

        for k in keys:
            if not isinstance(value, dict) or k not in value:
                raise KeyError(f"Config key not found: '{key}'")
            value = value[k]

        return value

    def reload(self) -> None:
        """Force reload config from file (useful if config changes)."""
        self._config = self._load_file()
        print("[ConfigManager] Config reloaded")

    @classmethod
    def reset(cls) -> None:
        """Reset the singleton (useful for testing)."""
        cls._instance = None


# ─────────────────────────────────────────────
# 2. Services (refactored to use the Singleton)
# ─────────────────────────────────────────────

class DatabaseService:
    def connect(self):
        config = ConfigManager.get_instance()
        host = config.get("database.host")
        port = config.get("database.port")
        print(f"Connecting to database at {host}:{port}")


class EmailService:
    def send_email(self, to: str, subject: str):
        config = ConfigManager.get_instance()
        smtp_host = config.get("email.smtp_host")
        sender = config.get("email.sender")
        print(f"Sending '{subject}' to {to} from {sender} via {smtp_host}")


class PaymentService:
    def process_payment(self, amount: float):
        config = ConfigManager.get_instance()
        api_key = config.get("payment.api_key")
        environment = config.get("payment.environment")
        print(f"Processing {amount}€ in {environment} mode (key: {api_key[:8]}...)")


# ─────────────────────────────────────────────
# Usage
# ─────────────────────────────────────────────

if __name__ == "__main__":

    print("=== Starting Application ===\n")

    # First call: loads the file
    config = ConfigManager.get_instance("config.json")
    app_name = config.get("app.name")
    debug = config.get("app.debug")
    print(f"Starting {app_name} (debug={debug})\n")

    # All these services reuse the SAME instance — no file reads
    print("--- Services calling get_instance() ---")
    db = DatabaseService()
    db.connect()

    email = EmailService()
    email.send_email("user@test.com", "Welcome")

    payment = PaymentService()
    payment.process_payment(99.99)

    # Proof: same instance everywhere
    print("\n--- Singleton proof ---")
    instance_1 = ConfigManager.get_instance()
    instance_2 = ConfigManager.get_instance()
    print(f"instance_1 is instance_2: {instance_1 is instance_2}")
    print(f"Same memory address: {id(instance_1)} == {id(instance_2)}")

    # Access a missing key
    print("\n--- Error handling ---")
    try:
        config.get("database.password")
    except KeyError as e:
        print(f"Error caught: {e}")
