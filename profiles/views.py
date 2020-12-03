from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from checkout.models import order
from .models import UserProfile
from .forms import UserProfileForm


@login_required
def profile_view(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid:
            form.save()
            messages.success(request, 'Profile Updated!')
        else:
            messages.error(request, 'Something went wrong, please check the form and try again.')
    else:
        form = UserProfileForm(instance=profile)
    orders = profile.orders.all()
    context = {
        'form': form,
        'orders': orders
    }
    template = 'profiles/my_profile.html'
    return render(request, template,  context)


def order_history(request, order_number):
    Order = get_object_or_404(order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': Order,
        'from_profile': True,
    }

    return render(request, template, context)

# https://github.com/ckz8780/boutique_ado_v1/blob/250e2c2b8e43cccb56b4721cd8a8bd4de6686546/profiles/views.py
