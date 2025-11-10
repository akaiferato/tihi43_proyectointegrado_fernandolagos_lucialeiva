from django import forms
from .models import Supplier

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['rut_nif', 'trade_name', 'company_name', 'email', 'telephone_number', 'direction', 'country']
