"""
Payment Factory Pattern - Refactored Solution
==============================================
Refactored from a single spaghetti if/elif function
into a clean Factory Pattern architecture following
the Open/Closed Principle (SOLID).
"""

from abc import ABC, abstractmethod


# ─────────────────────────────────────────────
# 1. The Interface (Abstract Base Class)
# ─────────────────────────────────────────────

class PaymentProcessor(ABC):
    """
    Abstract base class defining the contract
    that every payment processor must follow.
    """

    @abstractmethod
    def validate(self, details: dict) -> bool:
        """Validate payment details before processing."""
        pass

    @abstractmethod
    def process(self, amount: float, details: dict) -> dict:
        """Process the payment and return a result dict."""
        pass


# ─────────────────────────────────────────────
# 2. Concrete Implementations
# ─────────────────────────────────────────────

class CreditCardProcessor(PaymentProcessor):
    """Handles credit card payments with a 2.9% fee."""

    def __init__(self):
        self._fee_rate = 0.029

    def validate(self, details: dict) -> bool:
        card_number = details.get("card_number")
        cvv = details.get("cvv")

        if not card_number or len(card_number) != 16:
            raise ValueError("Invalid card number")
        if not cvv or len(cvv) != 3:
            raise ValueError("Invalid CVV")

        return True

    def process(self, amount: float, details: dict) -> dict:
        self.validate(details)
        fee = amount * self._fee_rate
        total = amount + fee
        return {
            "success": True,
            "method": "credit_card",
            "amount": round(total, 2),
            "fee": round(fee, 2)
        }


class BankTransferProcessor(PaymentProcessor):
    """Handles bank transfers with a flat 1.50€ fee."""

    def __init__(self):
        self._flat_fee = 1.50

    def validate(self, details: dict) -> bool:
        iban = details.get("iban")

        if not iban or len(iban) < 15:
            raise ValueError("Invalid IBAN")

        return True

    def process(self, amount: float, details: dict) -> dict:
        self.validate(details)
        fee = self._flat_fee
        total = amount + fee
        return {
            "success": True,
            "method": "bank_transfer",
            "amount": round(total, 2),
            "fee": round(fee, 2)
        }


class PayPalProcessor(PaymentProcessor):
    """Handles PayPal payments with a 3.4% + 0.30€ fee."""

    def __init__(self):
        self._fee_rate = 0.034
        self._fixed_fee = 0.30

    def validate(self, details: dict) -> bool:
        email = details.get("email")

        if not email or "@" not in email:
            raise ValueError("Invalid PayPal email")

        return True

    def process(self, amount: float, details: dict) -> dict:
        self.validate(details)
        fee = amount * self._fee_rate + self._fixed_fee
        total = amount + fee
        return {
            "success": True,
            "method": "paypal",
            "amount": round(total, 2),
            "fee": round(fee, 2)
        }


# ─────────────────────────────────────────────
# 3. The Factory
# ─────────────────────────────────────────────

class PaymentFactory:
    """
    Factory that maps payment type strings to
    their corresponding processor classes.
    Uses a dict instead of if/elif chains.
    """

    def __init__(self):
        self._processors = {
            "credit_card": CreditCardProcessor,
            "bank_transfer": BankTransferProcessor,
            "paypal": PayPalProcessor
        }

    def get_processor(self, payment_type: str) -> PaymentProcessor:
        """
        Returns an instance of the matching processor.
        Raises ValueError if the type is unknown.
        """
        processor_class = self._processors.get(payment_type)

        if not processor_class:
            raise ValueError(f"Unknown payment type: {payment_type}")

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
