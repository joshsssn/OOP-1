import json

class ConfigManager:
    _instance = None

    def __init__(self, config_path: str = "config.json"):
        self._config_path = config_path
        self._config = dict()

    @classmethod
    def get_instance(cls, config_path: str = "config.json") -> "ConfigManager":
        if cls._instance is None:
            cls._instance = ConfigManager(config_path)
            # Simulate loaded config
            cls._instance._config = {"database": {"host": "localhost", "port": 5432}}
        return cls._instance

    def get(self, key: str):
        keys = key.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return None
        return value

    def reload(self) -> None:
        pass

class DatabaseService:
    def connect(self) -> None:
        pass

class EmailService:
    def send_email(self, to: str, subject: str) -> None:
        pass

class PaymentService:
    def process_payment(self, amount: float) -> None:
        pass


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
