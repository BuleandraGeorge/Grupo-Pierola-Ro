import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings
from products.models import product, size


# Create your models here.
class order(models.Model):
    order_number = models.CharField(max_length=32, null=False, blank=False, editable=False)
    full_name = models.CharField(max_length=32, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=254, null=False, blank=False)
    street_address1 = models.CharField(max_length=254, null=False, blank=False)
    street_address2 = models.CharField(max_length=254, null=True, blank=True)
    town_or_city = models.CharField(max_length=254, null=False, blank=False)
    country = models.CharField(max_length=254, null=False, blank=False)
    postcode = models.CharField(max_length=40, null=False, blank=False)
    date = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

    def _generate_order_number(self):
        return uuid.uuid4().hex.upper()
    
    def update_total(self):
        self.total = self.orderLineItem.order.aggregate(Sum('line_total'))['line_total__sum']
        self.save()

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number

class orderLineItem(models.Model):
    order = models.ForeignKey(order, null=False, blank=False, on_delete=models.CASCADE)
    product = models.ForeignKey(product, null=False, blank=False, on_delete=models.CASCADE)
    product_size = models.ForeignKey(size, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    line_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        self.line_total = self.quantity * self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Product {self.product.name} on order {self.order.order_number}"