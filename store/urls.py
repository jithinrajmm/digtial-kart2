from django.urls import path
from store import views
app_name = 'store'

urlpatterns = [
    path('',views.store,name='Store'),
    path('<slug:slug>/',views.store,name='Store_slug'),
    path('<slug:category_slugs>/<slug:product_slug>/',views.single_product,name='single_product'),
]

