
from carts.models import Cart,CartItems
from carts.views import _get_cart_id



def cart_counter(request):
    count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_get_cart_id(request))
            if request.user.is_authenticated:
                cart_items = CartItems.objects.all().filter(user=request.user)
            else:
                cart_items = CartItems.objects.all().filter(cart=cart[:1])

            for item in cart_items:
                count = count + item.quantity  
     
        except Cart.DoesNotExist:
            count = 0
    return dict(cart_count=count)