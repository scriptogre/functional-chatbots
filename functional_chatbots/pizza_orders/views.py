from typing import Literal

from django.http import HttpResponse
from ninja import Router, Form
from pydantic import BaseModel

from functional_chatbots.pizza_orders.services import create_pizza_order, get_pizza_order, update_pizza_order, delete_pizza_order, \
    list_pizza_orders
from functional_chatbots.utils import render

"""
This file contains the CRUD views for pizza orders. 
"""


router = Router()


class PizzaOrderIn(BaseModel):
    name: Literal['cheese', 'pepperoni', 'vegetarian']
    size: Literal['small', 'medium', 'large']


# Read

@router.get('/pizza-orders')
def list_pizza_orders_view(request):
    """
    List all pizza orders.

    We just need to `hx-select` the #pizza-orders element from the index template.
    """
    pizza_orders = list_pizza_orders()
    return render(request, 'index', {'pizza_orders': pizza_orders})


# Create

@router.get('/pizza-orders/add')
def pizza_order_create_form_view(request):
    """Renders the form to create a new pizza order"""
    return render(request, 'pizza_order_create_form')


@router.post('/pizza-orders/add')
def pizza_order_create_view(request, payload: Form[PizzaOrderIn]):
    """Creates the pizza order"""
    create_pizza_order(request, payload)
    return HttpResponse(status=204, headers={'HX-Trigger': 'pizzaOrdersUpdated'})


# Update

@router.get('/pizza-orders/{order_id}/update')
def pizza_order_update_form_view(request, order_id: int):
    """Renders the form to update a pizza order"""
    pizza_order = get_pizza_order(request, order_id)
    return render(request, 'pizza_order_update_form', {'pizza_order': pizza_order})


@router.post('/pizza-orders/{order_id}/update')
def pizza_order_update_view(request, order_id: int, payload: Form[PizzaOrderIn]):
    """Updates the pizza order"""
    update_pizza_order(request, order_id, payload)
    return HttpResponse(status=204, headers={'HX-Trigger': 'pizzaOrdersUpdated'})


# Delete

@router.get('/pizza-orders/{order_id}/delete')
def pizza_order_delete_form_view(request, order_id: int):
    """Renders the form to delete a pizza order"""
    return render(request, 'pizza_order_delete_form', {'order_id': order_id})


@router.post('/pizza-orders/{order_id}/delete')
def pizza_order_delete_view(request, order_id: int):
    """Deletes the pizza order"""
    delete_pizza_order(request, order_id)
    return HttpResponse(status=204, headers={'HX-Trigger': 'pizzaOrdersUpdated'})

