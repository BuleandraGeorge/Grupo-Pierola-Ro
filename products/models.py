from django.db import models

# Create your models here.
from django.db import models

import datetime


class color(models.Model):
    name = models.CharField(max_length=254, blank=True, null=True)

    def __str__(self):
        return self.name



class grape_variety(models.Model):
    class Meta:
        verbose_name_plural = 'Grape Varieties'

    name = models.CharField(max_length=254, blank=True, null=True)

    def __str__(self):
        return self.name



class region(models.Model):
    name = models.CharField(max_length=254, blank=True, null=True)

    def __str__(self):
        return self.name



class size(models.Model):
    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name


class product(models.Model):
    name = models.CharField(max_length=254, null=False, blank=False)
    color = models.ForeignKey('color', null=True, blank=True, on_delete=models.SET_NULL)
    grape_variety = models.ForeignKey('grape_variety', null=True, blank=True, on_delete=models.SET_NULL)
    region = models.ForeignKey('region', null=True, blank=True, on_delete=models.SET_NULL)
    vinification = models.TextField(max_length=3000, null=True, blank=True)
    color_details = models.TextField(max_length=3000, null=True, blank=True)
    aroma = models.TextField(blank=True, null=True)
    palate = models.TextField(blank=True, null=True)
    ageing = models.TextField(blank=True, null=True)
    service = models.CharField(max_length=254,blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    size = models.ManyToManyField(size)
    box = models.CharField(max_length=254, null=True, blank=True)
    quantity_available = models.IntegerField(null=False, blank=False)
    total_quantity_sold = models.IntegerField(null=False, blank=False, default=0)
    first_listed = models.DateField(auto_now_add=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name