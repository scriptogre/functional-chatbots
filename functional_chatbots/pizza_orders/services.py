from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from functional_chatbots.pizza_orders.views import PizzaOrderIn

from functional_chatbots.pizza_orders.models import PizzaOrder


def create_pizza_order(payload: 'PizzaOrderIn') -> PizzaOrder:
    """
    This can include all the business logic for creating a pizza order. We could send an email, a notification, etc.
    """
    return PizzaOrder.objects.create(**payload.dict())


def get_pizza_order(order_id: int) -> PizzaOrder:
    return PizzaOrder.objects.get(id=order_id)


def list_pizza_orders():
    return PizzaOrder.objects.all()


def update_pizza_order(order_id: int, payload: 'PizzaOrderIn') -> PizzaOrder:
    pizza_order = PizzaOrder.objects.get(id=order_id)
    pizza_order.name = payload.name
    pizza_order.size = payload.size
    pizza_order.add_extra_time(30)
    return pizza_order.save()


def delete_pizza_order(order_id: int) -> None:
    pizza_order = PizzaOrder.objects.get(id=order_id)
    pizza_order.delete()
