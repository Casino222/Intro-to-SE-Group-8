from .models import Order

def view_order_history(user):
    return Order.objects.filter(user=user)

def track_order_status(order_id):
    try:
        order = Order.objects.get(pk=order_id)
        return order.status
    except Order.DoesNotExist:
        return None

