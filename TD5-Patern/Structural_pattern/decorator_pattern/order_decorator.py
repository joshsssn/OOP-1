from abc import ABC, abstractmethod

class OrderComponent(ABC):
    @abstractmethod
    def get_cost(self) -> float:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass

class BaseOrder(OrderComponent):
    def __init__(self, base_price: float):
        self._base_price = base_price

    def get_cost(self) -> float:
        return self._base_price

    def get_description(self) -> str:
        return f"Base order"

class OrderDecorator(OrderComponent, ABC):
    def __init__(self, wrapped: OrderComponent):
        self._wrapped = wrapped

    def get_cost(self) -> float:
        return self._wrapped.get_cost()

    def get_description(self) -> str:
        return self._wrapped.get_description()

class ExpressShippingDecorator(OrderDecorator):
    def get_cost(self) -> float:
        return super().get_cost() + 15.0

    def get_description(self) -> str:
        return super().get_description() + " + express shipping"

class InsuranceDecorator(OrderDecorator):
    def get_cost(self) -> float:
        return super().get_cost() * 1.05

    def get_description(self) -> str:
        return super().get_description() + " + insurance"

class GiftWrapDecorator(OrderDecorator):
    def get_cost(self) -> float:
        return super().get_cost() + 5.0

    def get_description(self) -> str:
        return super().get_description() + " + gift wrap"

class DiscountDecorator(OrderDecorator):
    def __init__(self, wrapped: OrderComponent, percent: float):
        super().__init__(wrapped)
        self._percent = percent

    def get_cost(self) -> float:
        return super().get_cost() * (1 - self._percent / 100)

    def get_description(self) -> str:
        return super().get_description() + f" - discount"

class PremiumMemberDecorator(OrderDecorator):
    def get_cost(self) -> float:
        return super().get_cost() * 0.90

    def get_description(self) -> str:
        return super().get_description() + " - premium discount"


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
