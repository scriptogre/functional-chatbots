from ninja import Router

from app.utils import render

from .services import list_pizza_orders

router = Router()


@router.get('/pizza-orders')
def list_pizza_orders_view(request):
    """Response for HTMX hx-get + hx-select=#pizza-orders."""
    if not request.session.session_key:
        request.session.save()
    orders = list_pizza_orders(request.session.session_key)
    return render(request, 'index', {'pizza_orders': orders})
