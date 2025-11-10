from django import forms
from .models import Product, Category, Brand
from django.core.exceptions import ValidationError

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'sku', 'ean_upc', 'name', 'description', 'category', 'brand', 'supplier',
            'model', 'uom_purchase', 'uom_sale', 'conversion_factor', 'price',
            'iva_tax', 'minimum_stock', 'maximum_stock', 'perishable',
            'batch_control', 'series_control', 'image_url', 'datasheet_url'
        ]

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise ValidationError("El precio debe ser mayor a 0.")
        return price

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name']
