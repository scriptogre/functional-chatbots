from typing import Annotated

from django.http import HttpResponse
from ninja import Form, Router

from main.utils import render

from .schemas import PizzaOrderIn
from .services import (
    create_pizza_order,
    delete_pizza_order,
    get_pizza_order,
    list_pizza_orders,
    update_pizza_order,
)

router = Router()


@router.get('/pizza-orders')
def list_pizza_orders_view(request):
    """List all orders. Used by `hx-get` + `hx-select=#pizza-orders`."""
    return render(request, 'index', {'pizza_orders': list_pizza_orders()})


@router.get('/pizza-orders/add')
def pizza_order_create_form(request):
    return render(request, 'partials/pizza_order_create_form')


@router.post('/pizza-orders/add')
def pizza_order_create(request, payload: Annotated[PizzaOrderIn, Form()]):
    create_pizza_order(payload)
    return HttpResponse(status=204, headers={'HX-Trigger': 'pizzaOrdersUpdated'})


@router.get('/pizza-orders/{order_id}/update')
def pizza_order_update_form(request, order_id: int):
    return render(
        request,
        'partials/pizza_order_update_form',
        {'pizza_order': get_pizza_order(order_id)},
    )


@router.post('/pizza-orders/{order_id}/update')
def pizza_order_update(request, order_id: int, payload: Annotated[PizzaOrderIn, Form()]):
    update_pizza_order(order_id, payload)
    return HttpResponse(status=204, headers={'HX-Trigger': 'pizzaOrdersUpdated'})


@router.get('/pizza-orders/{order_id}/delete')
def pizza_order_delete_form(request, order_id: int):
    return render(request, 'partials/pizza_order_delete_form', {'order_id': order_id})


@router.post('/pizza-orders/{order_id}/delete')
def pizza_order_delete(request, order_id: int):
    delete_pizza_order(order_id)
    return HttpResponse(status=204, headers={'HX-Trigger': 'pizzaOrdersUpdated'})
