"""GPR URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls')),
    path('', include('user_filter.urls')),
    path('wines/', include('products.urls')),
    path('bag/', include('bag.urls')),
    path('checkout/', include('checkout.urls')),
    path('my_profile/', include('profiles.urls'),),
    path('contact/', include('contact.urls'),),
    path('about/', include('about.urls'),)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
