

from django.shortcuts import render
from adminpanel.models import CategoryOffer
from carts.models import CartItems
from category.models import Category
from store.models import Product
from django.db.models import Q
from carts.views import _get_cart_id
from django.core.paginator import Paginator


# Create your views here.

def store(request,slug=None):

    if slug:
        products = Product.objects.filter(Q(slug__icontains=slug)| Q(category__category_slug__icontains=slug))
        product_count = products.count()

    elif request.GET.get('serching_word'):
        key_word = request.GET.get('serching_word')
        products = Product.objects.filter(Q(slug__icontains=key_word)
                                        | Q(category__category_slug__icontains=key_word)
                                        | Q(category__category_name__icontains=key_word)
                                        | Q(product_name__icontains=key_word)
                                        | Q(description__icontains=key_word)
                                        | Q(price__icontains=key_word))

        product_count = products.count()

    else:
        products = Product.objects.all()
        product_count = products.count()

    products_paginater = Paginator(products,6)
    page_number = request.GET.get('page')
    product_objects  = products_paginater.get_page(page_number) 

    context = {
        'products': product_objects,
        'product_count':product_count,
    }
    return render(request,'home/shop.html',context)


def single_product(request,category_slugs,product_slug):
  
    try:
        product = Product.objects.get(category__category_slug=category_slugs,slug=product_slug)
        product_in_cart = CartItems.objects.filter(cart__cart_id=_get_cart_id(request),product=product).exists()
        
    except Exception as e:
        raise e
    
    context={
        'product':product,
        'product_id_cart':product_in_cart,
    }

    return render(request,'home/singleproductview.html',context)
