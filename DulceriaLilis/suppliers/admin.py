from django.contrib import admin
from .models import Supplier


@admin.register(Supplier)
class supplierAdmin(admin.ModelAdmin):
    list_display = ('rut_nif',
                    'trade_name',
                    'email',
                    'country',
                    'pay_conditions',
                    'currency')
    list_filter = ('country',
                   'currency')
    search_fields = ('rut_nif',
                     'trade_name',
                     'email')
    ordering = ('rut_nif',)

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        roles = [group.name for group in request.user.groups.all()]
        if 'Bodega' in roles:
            return False
        return True
