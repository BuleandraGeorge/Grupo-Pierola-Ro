from django.shortcuts import render, redirect
from decorators import adult_or_logged_in
from products.models import product
# Create your views here.

@adult_or_logged_in
def home(request):
    products = product.objects.all()
    most_sold= products.order_by('-total_quantity_sold')[:4]
    new_arrivals = products.order_by('first_listed')[:4]
    best_rating = products.order_by('-rating')[:4]
    context ={
        'most_sold': most_sold,
        'new_arrivals' : new_arrivals,
        'best_rating': best_rating
    }
    return render(request, "home/home.html", context)