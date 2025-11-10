from django import forms
from .models import Cellar, inventoryMovement

class CellarForm(forms.ModelForm):
    class Meta:
        model = Cellar
        fields = ['cellar_name', 'location']

class InventoryMovementForm(forms.ModelForm):
    class Meta:
        model = inventoryMovement
        fields = ['product', 'cellar', 'user', 'supplier', 'movement_type', 'quantity', 'batch', 'serie', 'caducity_date']
