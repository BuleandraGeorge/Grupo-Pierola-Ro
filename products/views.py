from django.shortcuts import render, get_object_or_404
from .models import product

# Create your views here.

def products(request):

    products = product.objects.all()
    context = {
        "products": products
    }
    return render(request, 'products/products.html', context)


def product_details(request, product_id):

    wine = get_object_or_404(product, pk=product_id)
    context = {
        "product": wine
    }
    return render(request, 'products/product_details.html', context)