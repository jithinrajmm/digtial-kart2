from orders.models import OrderProduct


def order_product(request):
    
    if request.user.is_authenticated:
        order_product= OrderProduct.objects.filter(user=request.user,ordered=True)
    else:
        order_product ={}

    context={
        'order_product':order_product,
    }

    return context

def cancelled_orders_product(request):
    if request.user.is_authenticated:
        cancelled_product= OrderProduct.objects.filter(user=request.user,ordered=False,order__status='Cancelled')
    else:
        cancelled_product ={}

    context={
        'cancelled_product':cancelled_product,
    }

    return context

