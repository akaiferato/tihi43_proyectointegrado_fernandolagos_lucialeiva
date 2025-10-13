from django.contrib import admin
from .models import inventoryMovement, movementType, Cellar


@admin.register(Cellar)
class cellarAdmin(admin.ModelAdmin):
    list_display = ('cellar_name',
                    'created_at',
                    'updated_at',)
    search_fields = ('cellar_name',)
    list_filter = ('created_at',)
    ordering = ('cellar_name',)


@admin.register(movementType)
class MovementTypeAdmin(admin.ModelAdmin):
    list_display = ('movement_type',
                    'created_at',
                    'updated_at',)
    search_fields = ('movement_type',)
    list_filter = ('created_at',)
    ordering = ('movement_type',)


@admin.register(inventoryMovement)
class InventoryMovementAdmin(admin.ModelAdmin):
    list_display = ('product',
                    'cellar',
                    'user',
                    'supplier',
                    'movement_type',
                    'datetime',
                    'quantity',
                    )
    search_fields = ('product',
                     'movement_type',)
    list_filter = ('cellar',
                   'supplier',)
    ordering = ('movement_type',)
    list_select_related = ('product',
                           'cellar',
                           'user',
                           'supplier',
                           'movement_type',)
