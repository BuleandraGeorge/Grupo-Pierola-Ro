from django.db import models

# Create your models here.
from django.db import models


class colors(models.Model):
    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name


class grape_variety(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.name


class region(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.name


class size(models.Model):
    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.name


class product(models.Model):
    name = models.CharField(max_length=254, null=False, blank=False)
    color = models.ForeignKey('colors', null=True, blank=True, on_delete=models.SET_NULL)
    grape_variety = models.ForeignKey('grape_variety', null=True, blank=True, on_delete=models.SET_NULL)
    region = models.ForeignKey('region', null=True, blank=True, on_delete=models.SET_NULL)
    vinification = models.TextField(max_length=3000, null=True, blank=True)
    color_details = models.TextField(max_length=3000, null=True, blank=True)
    aroma = models.TextField()
    palate = models.TextField()
    ageing = models.TextField()
    service = models.CharField(max_length=254)
    price = models.DecimalField(max_digits=4, decimal_places=2, null=False, blank=False)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    size = models.ManyToManyField(size)
    box = models.CharField(max_length=254, null=True, blank=True)
    quantity_available = models.IntegerField(null=False, blank=False)
    total_quantity_sold = models.IntegerField(null=False, blank=False)
    first_listed = models.DateField(default="2020/01/01")
    image = models.ImageField(null=False, blank=False)

    def __str__(self):
        return self.name