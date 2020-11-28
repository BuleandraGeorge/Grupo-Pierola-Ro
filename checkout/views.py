from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from products.models import product, size
from .forms import orderForm
from bag.contexts import bag_content
from .models import orderLineItem, order
from profiles.models import UserProfile
from profiles.forms import UserProfileForm

import stripe
import json


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'username': request.user,
            'save_info': request.POST.get('save_info'),
            'bag': json.dumps(request.session.get('bag', {}))
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be procced right now \
        Please, try again later.')
        return HttpResponse(content=e, status=400)


def checkout_view(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == "POST":
        bag = request.session.get('bag', {})
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'town_or_city': request.POST['town_or_city'],
            'postcode': request.POST['postcode'],
            'country': request.POST['country'],
        }
        order_form = orderForm(form_data)
        if order_form.is_valid:
            order = order_form.save(commit=False)
            order.stripe_pid = request.POST.get('client_secret').split('_secret')[0]
            order.original_bag = json.dumps(bag)
            full_name = request.POST['full_name'],
            email = request.POST['email'],
            phone_number = request.POST['phone_number'],
            street_address1 = request.POST['street_address1'],
            street_address2 = request.POST['street_address2'],
            town_or_city = request.POST['town_or_city'],
            postcode = request.POST['postcode'],
            country = request.POST['country'],
            order.save()
            for item_id, item_data in bag.items():
                try:
                    Product = get_object_or_404(product, pk=item_id)
                    for Size, quantity in item_data['item_size-quantity'].items():
                        orderline = orderLineItem(
                            order=order,
                            product=Product,
                            product_size=size.objects.get(name=Size),
                            quantity=quantity,
                        )
                        orderline.save()
                except product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))

            request.session['save-info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form')
    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('products'))

        current_bag = bag_content(request)
        total = current_bag['total']
        total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=total,
            currency=settings.STRIPE_CURRENCY,
        )
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = orderForm(initial={
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                    'town_or_city': profile.default_town_or_city,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                })
            except UserProfile.DoesNotExist:
                order_form = orderForm()
        else:
            order_form = orderForm()

        template = 'checkout/checkout.html'
        context = {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
        }
        return render (request, template, context)


def checkout_success(request, order_number):
    Order = get_object_or_404(order, order_number=order_number)
    if request.user.is_authenticated:
        save_info = request.session.get('save_info')
        profile = UserProfile.objects.get(user=request.user)
        Order.user_profile = profile
        Order.save()
        if save_info:
            profile_data = {
                'default_phone_number': Order.phone_number,
                'default_country': Order.country,
                'default_postcode': Order.postcode,
                'default_town_or_city': Order.town_or_city,
                'default_street_address1': Order.street_address1,
                'default_street_address2': Order.street_address2,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. \
        An confirmations will send to {Order.email}')
    if 'bag' in request.session:
        del request.session['bag']
    context={
        'order': Order,
    }
    template = 'checkout/checkout_success.html'
    return render(request, template, context)