from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.db.models import Q
from .models import product, color, grape_variety, region

# Create your views here.

def products(request):

    products = product.objects.all()
    colors = color.objects.all()
    grapes = grape_variety.objects.all()
    regions = region.objects.all()

    query = None
    color_search = None
    region_search = None
    grape_search = None
    sort = None
    direction = None

    if request.GET:
        if 'grape' in request.GET:
            grape_search = request.GET['grape']
            products = products.filter(grape_variety__name=grape_search)

        if 'region' in request.GET:
            region_search = request.GET['region']
            products = products.filter(region__name=region_search)

        if 'color' in request.GET:
            color_search = request.GET['color']
            products = products.filter(color__name=color_search)
            print(color_search)

        if 'sort' in request.GET:
            sort = request.GET['sort']
            direction = request.GET['direction']
            if direction == 'desc':
                sort = f'-{sort}'
            products = products.order_by(sort)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria")
                return redirect(reverse('products'))
            queries = Q(name__icontains=query) | Q(palate__icontains=query)
            products = products.filter(queries)

    context = {
        "products": products,
        "search-term": query,
        "colors": colors,
        "grapes": grapes,
        "regions": regions,
        "color_search": color_search,
        "region_search": region_search,
        "grape_search": grape_search,
        "sort": sort,
        "direction": direction,

    }
    return render(request, 'products/products.html', context)


def product_details(request, product_id):

    wine = get_object_or_404(product, pk=product_id)
    context = {
        "product": wine
    }
    return render(request, 'products/product_details.html', context)