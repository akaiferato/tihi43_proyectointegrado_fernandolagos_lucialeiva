from django.contrib import admin
from django.utils import timezone
from .models import Category, Product, Brand, Supplier, productSupplier


class ProductSupplierInline(admin.TabularInline):
    model = productSupplier
    extra = 1
    fields = ('product',
              'supplier',
              'cost',
              'lead_time',
              'preferential')
    autocomplete_fields = ['supplier']


@admin.register(Category)
class categoryAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'created_at',
                    'updated_at')
    search_fields = ('name')
    list_filter = ('created_at')
    ordering = ('name')


@admin.register(Product)
class productAdmin(admin.ModelAdmin):
    list_display = ('sku',
                    'name',
                    'category',
                    'brand',
                    'price',
                    'perishable')
    search_fields = ('name',
                     'sku')
    list_filter = ('category',
                   'brand')
    ordering = ('name')
    list_select_related = ('category',
                           'brand')
    inlines = [ProductSupplierInline]
    actions = ['mark_perishable']

    @admin.action(description='Marcar productos como posible caducacion')
    def mark_perishable(self, request, queryset):
        updated = queryset.update(perishable=True,
                                  updated_at=timezone.now())
        self.message_user(request,
                          f"{updated} productos fueron marcados como posible caducacion.")


@admin.register(Brand)
class brandAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'created_at',
                    'updated_at')
    search_fields = ('name')
    list_filter = ('created_at')
    ordering = ('name')
