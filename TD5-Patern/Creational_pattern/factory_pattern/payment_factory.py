from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def validate(self, details: dict) -> bool:
        pass

    @abstractmethod
    def process(self, amount: float, details: dict) -> dict:
        pass

class CreditCardProcessor(PaymentProcessor):
    def __init__(self):
        self._fee_rate = 0.029

    def validate(self, details: dict) -> bool:
        return True

    def process(self, amount: float, details: dict) -> dict:
        self.validate(details)
        return {"success": True, "amount": amount + (amount * self._fee_rate)}

class BankTransferProcessor(PaymentProcessor):
    def __init__(self):
        self._flat_fee = 1.50

    def validate(self, details: dict) -> bool:
        return True

    def process(self, amount: float, details: dict) -> dict:
        self.validate(details)
        return {"success": True, "amount": amount + self._flat_fee}

class PayPalProcessor(PaymentProcessor):
    def __init__(self):
        self._fee_rate = 0.034
        self._fixed_fee = 0.30

    def validate(self, details: dict) -> bool:
        return True

    def process(self, amount: float, details: dict) -> dict:
        self.validate(details)
        return {"success": True, "amount": amount + (amount * self._fee_rate) + self._fixed_fee}

class PaymentFactory:
    def __init__(self):
        self._processors = {
            "credit_card": CreditCardProcessor,
            "bank_transfer": BankTransferProcessor,
            "paypal": PayPalProcessor
        }

    def get_processor(self, payment_type: str) -> PaymentProcessor:
        processor_class = self._processors.get(payment_type)
        if not processor_class:
            raise ValueError("Unknown payment type")
        return processor_class()

    def register(self, payment_type: str, processor_class: type) -> None:
        """
        Register a new payment processor at runtime.
        This is what makes the pattern truly Open/Closed —
        you can extend without modifying existing code.
        """
        if not issubclass(processor_class, PaymentProcessor):
            raise TypeError(f"{processor_class} must inherit from PaymentProcessor")
        self._processors[payment_type] = processor_class


# ─────────────────────────────────────────────
# Usage
# ─────────────────────────────────────────────

if __name__ == "__main__":

    factory = PaymentFactory()

    # Test credit card
    print("=== Credit Card ===")
    processor = factory.get_processor("credit_card")
    result = processor.process(100.0, {
        "card_number": "1234567890123456",
        "expiry": "12/25",
        "cvv": "123"
    })
    print(result)

    # Test bank transfer
    print("\n=== Bank Transfer ===")
    processor = factory.get_processor("bank_transfer")
    result = processor.process(100.0, {
        "iban": "FR7630006000011234567890189",
        "bic": "BNPAFRPP"
    })
    print(result)

    # Test PayPal
    print("\n=== PayPal ===")
    processor = factory.get_processor("paypal")
    result = processor.process(100.0, {
        "email": "jawad@example.com"
    })
    print(result)

    # Test unknown type
    print("\n=== Unknown Type ===")
    try:
        processor = factory.get_processor("bitcoin")
    except ValueError as e:
        print(f"Error: {e}")

    # ─── Demonstrate extensibility ───
    # Adding Apple Pay without touching ANY existing code
    print("\n=== Adding Apple Pay (runtime registration) ===")

    class ApplePayProcessor(PaymentProcessor):
        def __init__(self):
            self._fee_rate = 0.025

        def validate(self, details: dict) -> bool:
            if not details.get("device_token"):
                raise ValueError("Invalid device token")
            return True

        def process(self, amount: float, details: dict) -> dict:
            self.validate(details)
            fee = amount * self._fee_rate
            return {
                "success": True,
                "method": "apple_pay",
                "amount": round(amount + fee, 2),
                "fee": round(fee, 2)
            }

    factory.register("apple_pay", ApplePayProcessor)
    processor = factory.get_processor("apple_pay")
    result = processor.process(100.0, {"device_token": "abc123xyz"})
    print(result)
