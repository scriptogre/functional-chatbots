"""Pizza order CRUD. All operations scoped to session_key."""
from .models import PizzaOrder
from .schemas import PizzaFlavor, PizzaSize


def create_pizza_order(flavor: PizzaFlavor, size: PizzaSize, *, session_key: str = '') -> PizzaOrder:
    """Create a new pizza order with the given flavor and size."""
    return PizzaOrder.objects.create(name=flavor, size=size, session_key=session_key)


def update_pizza_order(
    pizza_order_id: str, flavor: PizzaFlavor, size: PizzaSize, *, session_key: str = '',
) -> PizzaOrder | None:
    """Update an existing pizza order. pizza_order_id comes from [Current State]."""
    pizza_order = PizzaOrder.objects.filter(id=pizza_order_id, session_key=session_key).first()
    if pizza_order is None:
        return None
    pizza_order.name = flavor
    pizza_order.size = size
    pizza_order.add_extra_time(30)
    pizza_order.save()
    return pizza_order


def delete_pizza_order(pizza_order_id: str, *, session_key: str = '') -> None:
    """Cancel an existing pizza order."""
    PizzaOrder.objects.filter(id=pizza_order_id, session_key=session_key).delete()


def list_pizza_orders(session_key: str):
    return PizzaOrder.objects.filter(session_key=session_key).order_by('id')


def delete_all_pizza_orders(session_key: str) -> None:
    PizzaOrder.objects.filter(session_key=session_key).delete()
