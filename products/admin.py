from django.contrib import admin
from .models import colors, grape_variety, region, size, product

admin.site.register(colors)
admin.site.register(grape_variety)
admin.site.register(region)
admin.site.register(size)
admin.site.register(product)

# Register your models here.
