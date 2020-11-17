
from django.urls import path
from .views import products, product_details

urlpatterns = [
    path('wines/', products, name='products'),
    path('wines/<product_id>', product_details, name='product_details'),
 
]