from django.shortcuts import render
from django.contrib import messages
from .forms import orderForm


def checkout_view(request):
    bag= request.session.get('bag',{})
    if not bag:
        return messages(request, "There is nothing in the bag")
    else:
        order_form = orderForm
        template = 'checkout/checkout.html'
        context = {
            'order_form': order_form,
            'stripe_public_key': 'pk_test_51Hr14BJ9ilEQDcKTpaKRQtlhpdeBX5kDVzzwzmIDxKKznqEfsvOYA5YmmsXxYNC2Vobz2sFBQ6EdTalsH146yGLB00rJYkVRaF',
            'client_secret': 'test client secret',
        }
        return render (request, template, context)
