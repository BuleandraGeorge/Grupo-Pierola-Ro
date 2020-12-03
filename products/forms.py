from django import forms
from .models import product, size, grape_variety, region, color
from .widgets import CustomClearableFileInput


class formProduct (forms.ModelForm):

    class Meta:
        model = product
        exclude = {'total_quantity_sold'}

    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Adds min and max values for inputs where is need it
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-danger rounded-0'
            if field_name == 'quantity_available':
                field.widget.attrs['min'] = 1
            if field_name == 'price':
                field.widget.attrs['min'] = 1
                field.widget.attrs['max'] = 9999.99
            if field_name == 'rating':
                field.widget.attrs['min'] = 1
                field.widget.attrs['max'] = 5
