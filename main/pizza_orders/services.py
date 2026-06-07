"""Pizza order business logic. Called by views and by the LLM dispatcher."""
from .models import PizzaOrder
from .schemas import PizzaOrderIn


def create_pizza_order(payload: PizzaOrderIn) -> PizzaOrder:
    return PizzaOrder.objects.create(name=payload.name, size=payload.size)


def get_pizza_order(order_id: int) -> PizzaOrder:
    return PizzaOrder.objects.get(id=order_id)


def list_pizza_orders():
    return PizzaOrder.objects.all().order_by('id')


def update_pizza_order(order_id: int, payload: PizzaOrderIn) -> PizzaOrder:
    pizza_order = PizzaOrder.objects.get(id=order_id)
    pizza_order.name = payload.name
    pizza_order.size = payload.size
    pizza_order.add_extra_time(30)
    pizza_order.save()
    return pizza_order


def delete_pizza_order(order_id: int) -> None:
    PizzaOrder.objects.filter(id=order_id).delete()
