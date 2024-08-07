from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from functional_chatbots.pizza_orders.views import PizzaOrderIn

from functional_chatbots.pizza_orders.models import PizzaOrder


def create_pizza_order(request, payload: 'PizzaOrderIn') -> PizzaOrder:
    """
    This can include all the business logic for creating a pizza order. We could send an email, a notification, etc.
    """
    return PizzaOrder.objects.create(**payload.dict(), session_key=request.session.session_key)


def get_pizza_order(request, order_id: int) -> PizzaOrder:
    return PizzaOrder.objects.get(id=order_id, session_key=request.session.session_key)


def list_pizza_orders():
    return PizzaOrder.objects.all()


def update_pizza_order(request, order_id: int, payload: 'PizzaOrderIn') -> PizzaOrder:
    pizza_order = PizzaOrder.objects.filter(id=order_id, session_key=request.session.session_key).first()
    if pizza_order:
        pizza_order.name = payload.name
        pizza_order.size = payload.size
        pizza_order.add_extra_time(30)
        pizza_order.save()
    return pizza_order


def delete_pizza_order(request, order_id: int) -> dict[str, bool]:
    if pizza_order := PizzaOrder.objects.filter(id=order_id, session_key=request.session.session_key).first():
        pizza_order.delete()
    return {"success": True}
