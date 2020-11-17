from django.urls import path
from . import views

urlpatterns = [
    path('bag/', views.bag, name='bag'),
    path('bag/<item_id>', views.add_to_bag, name='add_to_bag'),
    path('modify/<item_id>', views.modify_quantity, name='modify_quantity'),
    path('remove/<item_id>/', views.remove_item, name='remove_item'),
]