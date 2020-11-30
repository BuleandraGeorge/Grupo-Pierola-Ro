from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.db.models import Q
from .models import product, color, grape_variety, region, size
from .forms import formProduct

# Create your views here.

def products(request):

    products = product.objects.all()
    colors = color.objects.all()
    grapes = grape_variety.objects.all()
    regions = region.objects.all()
    sizes = size.objects.all()

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
        "sizes": sizes,

    }
    return render(request, 'products/products.html', context)


def product_details(request, product_id):

    wine = get_object_or_404(product, pk=product_id)
    context = {
        "product": wine
    }
    return render(request, 'products/product_details.html', context)


def add_product(request):
    if request.method == "POST":
        form = formProduct(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product {request.POST["name"]}  has been added.')
            return redirect(reverse('add_product'))
        else:
            messages.error(request, 'Something is wrong with the form, please check and try again')
    else:
        form = formProduct
    template = 'products/add_product.html'
    context = {
        'form': form
    }
    return render(request, template, context)


def edit_product(request, product_id):
    product_for_edit = get_object_or_404(product, pk=product_id)
    if request.method == "POST":
        form = formProduct(request.POST, request.FILES, instance=product_for_edit)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product {request.POST["name"]} has been edited.')
            return redirect(reverse('product_details', args=[product_for_edit.id]))
        else:
            messages.error(request, 'Something is wrong with the form, please check and try again')
    else:
        messages.info(request, f'You are eddinng product {product_for_edit.name}')
        form = formProduct(instance=product_for_edit)
    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product_for_edit
    }
    return render(request, template, context)

def delete_product(request, product_id):
    product_to_be_deleted = get_object_or_404(product, pk=product_id)
    product_to_be_deleted.delete()
    messages.success(request, f'Product {product_to_be_deleted} has been deleted!')
    return redirect(reverse('products'))
