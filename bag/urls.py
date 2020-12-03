from django.urls import path
from . import views

urlpatterns = [
    path('', views.bag, name='bag'),
    path('<item_id>', views.add_to_bag, name='add_to_bag'),
    path('<item_id>/', views.modify_quantity, name='modify_quantity'),
    path('<item_id>/', views.remove_item, name='remove_item'),
]