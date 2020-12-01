from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from profiles.models import UserProfile
from products.models import size, product
from .models import order as Order
from .models import orderLineItem
import json
import time


class StripeWH_Handler:

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_emails_subject.txt',
            {'order': order}
        )
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_emails_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL}
        )
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def handler_event(self, event):
        return HttpResponse(
                    content=f'Unhandled received: {event["type"]}',
                    status=200
                )

    def handler_intent_succeeded(self, event):
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info
        shipping = intent.shipping
        billing_details = intent.charges.data[0].billing_details
        total = round(intent.charges.data[0].amount / 100, 2)

        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.default_phone_number = shipping.phone
                profile.default_country = shipping.address.country
                profile.default_postcode = shipping.address.postal_code
                profile.default_town_or_city = shipping.address.city
                profile.default_street_address1 = shipping.address.line1
                profile.default_street_address2 = shipping.address.line2
                profile.save()

        for field, value in shipping.address.items():
            if value == "":
                shipping.address[field] = None

        order_exists = False
        attempt = 1
        while attempt < 5:
            try:
                order = Order.objects.get(
                    stripe_pid__iexact=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                order= Order.objects.all()
                attempt += 1
                time.sleep(1)
        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Handled WebHook received: {event["type"]} SUCCESS: Verified order already in db', status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                        full_name=shipping.name,
                        email=billing_details.email,
                        phone_number=shipping.phone,
                        street_address1=shipping.address.line1,
                        street_address2=shipping.address.line2,
                        postcode=shipping.address.postal_code,
                        town_or_city=shipping.address.city,
                        country=shipping.address.country,
                        total=total,
                        stripe_pid=pid,
                )
                for item_id, item_data in json.loads(bag).items():
                    Product = product.objects.get(id=item_id)
                    for Size, quantity in item_data['item_size-quantity'].items():
                        orderline = orderLineItem(
                            order=order,
                            product=Product,
                            product_size=size.objects.get(name=Size),
                            quantity=quantity
                        )
                        orderline.save()
            except Exception as e:
                if order:
                        order.delete()
                return HttpResponse(content=f'Web hook received: {event["type"]} \
                        | ERROR: {e}', status=500)
            self._send_confirmation_email(order)
        return HttpResponse(
                    content=f'Handled WebHook received: {event["type"]}\
                        | SUCCESS: Order created in webhook',
                    status=200
                )

    def handler_intent_failed(self, event):
        return HttpResponse(
                    content=f'Handled WebHook received: {event["type"]} ',
                    status=200
                )
