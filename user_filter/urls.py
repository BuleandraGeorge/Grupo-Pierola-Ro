from django.urls import path
from . import views

urlpatterns = [
    path('check_age/', views.check_age, name='checkage'),
    path('under_age/', views.under_age, name='underage'),
]
