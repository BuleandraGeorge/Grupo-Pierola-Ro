
from django.urls import path
from .views import products, product_details

urlpatterns = [
    path('wines/', products, name='product'),
    path('<product_id>', product_details, name='product_details'),
 
]