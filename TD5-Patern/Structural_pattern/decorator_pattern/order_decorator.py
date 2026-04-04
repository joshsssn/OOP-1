"""
Decorator Pattern - Order Pricing System
=========================================
Refactored from a single method with boolean flag explosion
into stackable Decorators that each add one feature to an order.
Each decorator wraps the previous one like layers of an onion.
"""

from abc import ABC, abstractmethod


# ─────────────────────────────────────────────
# 1. The Interface (component)
# ─────────────────────────────────────────────

class OrderComponent(ABC):
    """
    Contract for all orders and decorators.
    Both BaseOrder and every decorator implement this.
    """

    @abstractmethod
    def get_cost(self) -> float:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass


# ─────────────────────────────────────────────
# 2. The Base (concrete component)
# ─────────────────────────────────────────────

class BaseOrder(OrderComponent):
    """Simple order with just a base price."""

    def __init__(self, base_price: float):
        self._base_price = base_price

    def get_cost(self) -> float:
        return self._base_price

    def get_description(self) -> str:
        return f"Base order: {self._base_price}€"


# ─────────────────────────────────────────────
# 3. Abstract Decorator (common wrapper logic)
# ─────────────────────────────────────────────

class OrderDecorator(OrderComponent, ABC):
    """
    Base decorator that wraps any OrderComponent.
    All concrete decorators inherit from this.
    """

    def __init__(self, wrapped: OrderComponent):
        self._wrapped = wrapped

    def get_cost(self) -> float:
        return self._wrapped.get_cost()

    def get_description(self) -> str:
        return self._wrapped.get_description()


# ─────────────────────────────────────────────
# 4. Concrete Decorators (one per feature)
# ─────────────────────────────────────────────

class ExpressShippingDecorator(OrderDecorator):
    """Adds flat 15€ express shipping fee."""

    def __init__(self, wrapped: OrderComponent):
        super().__init__(wrapped)
        self._shipping_cost = 15.00

    def get_cost(self) -> float:
        return self._wrapped.get_cost() + self._shipping_cost

    def get_description(self) -> str:
        return self._wrapped.get_description() + f"\n  + Express shipping: +{self._shipping_cost}€"


class InsuranceDecorator(OrderDecorator):
    """Adds 5% insurance based on current cost."""

    def __init__(self, wrapped: OrderComponent):
        super().__init__(wrapped)
        self._rate = 0.05

    def get_cost(self) -> float:
        current = self._wrapped.get_cost()
        return current + (current * self._rate)

    def get_description(self) -> str:
        insurance_amount = self._wrapped.get_cost() * self._rate
        return self._wrapped.get_description() + f"\n  + Insurance (5%): +{insurance_amount:.2f}€"


class GiftWrapDecorator(OrderDecorator):
    """Adds flat 5€ gift wrapping fee."""

    def __init__(self, wrapped: OrderComponent):
        super().__init__(wrapped)
        self._wrap_cost = 5.00

    def get_cost(self) -> float:
        return self._wrapped.get_cost() + self._wrap_cost

    def get_description(self) -> str:
        return self._wrapped.get_description() + f"\n  + Gift wrap: +{self._wrap_cost}€"


class DiscountDecorator(OrderDecorator):
    """Applies a percentage discount on current total."""

    def __init__(self, wrapped: OrderComponent, percent: float):
        super().__init__(wrapped)
        self._percent = percent

    def get_cost(self) -> float:
        current = self._wrapped.get_cost()
        return current - (current * self._percent / 100)

    def get_description(self) -> str:
        discount_amount = self._wrapped.get_cost() * self._percent / 100
        return self._wrapped.get_description() + f"\n  - Discount ({self._percent}%): -{discount_amount:.2f}€"


class PremiumMemberDecorator(OrderDecorator):
    """Applies a 10% premium member discount."""

    def __init__(self, wrapped: OrderComponent):
        super().__init__(wrapped)
        self._discount_rate = 0.10

    def get_cost(self) -> float:
        current = self._wrapped.get_cost()
        return current - (current * self._discount_rate)

    def get_description(self) -> str:
        discount_amount = self._wrapped.get_cost() * self._discount_rate
        return self._wrapped.get_description() + f"\n  - Premium member (10%): -{discount_amount:.2f}€"


# ─────────────────────────────────────────────
# Usage
# ─────────────────────────────────────────────

if __name__ == "__main__":

    # ── Simple order (no extras) ──
    print("=== Simple Order ===")
    order = BaseOrder(100.00)
    print(order.get_description())
    print(f"TOTAL: {order.get_cost():.2f}€")

    # ── Complex order (stacked decorators) ──
    print("\n=== Complex Order ===")
    order = BaseOrder(100.00)
    order = ExpressShippingDecorator(order)
    order = InsuranceDecorator(order)
    order = GiftWrapDecorator(order)
    order = DiscountDecorator(order, percent=15)
    order = PremiumMemberDecorator(order)

    print(order.get_description())
    print(f"TOTAL: {order.get_cost():.2f}€")

    # ── Different combo (just shipping + premium) ──
    print("\n=== Shipping + Premium Only ===")
    order = BaseOrder(200.00)
    order = ExpressShippingDecorator(order)
    order = PremiumMemberDecorator(order)

    print(order.get_description())
    print(f"TOTAL: {order.get_cost():.2f}€")

    # ── Order of decorators matters! ──
    print("\n=== Order matters: discount BEFORE vs AFTER shipping ===")

    # Discount first, then shipping
    order_a = BaseOrder(100.00)
    order_a = DiscountDecorator(order_a, percent=50)
    order_a = ExpressShippingDecorator(order_a)
    print(f"Discount then shipping: {order_a.get_cost():.2f}€")

    # Shipping first, then discount
    order_b = BaseOrder(100.00)
    order_b = ExpressShippingDecorator(order_b)
    order_b = DiscountDecorator(order_b, percent=50)
    print(f"Shipping then discount: {order_b.get_cost():.2f}€")
