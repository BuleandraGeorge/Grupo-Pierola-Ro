from django.contrib import admin
from .models import order, orderLineItem

class orderLineItemAdminline(admin.TabularInline):
    model = orderLineItem
    readonly_fields = ('line_total',)

class OrderAdmin(admin.ModelAdmin):
    inlines = (orderLineItemAdminline,)
    readonly_fields = ('order_number', 'date', 'total', )
    list_display = ('order_number','full_name', 'date', 'total',)
    ordering = ('-date',)

admin.site.register(order, OrderAdmin)
