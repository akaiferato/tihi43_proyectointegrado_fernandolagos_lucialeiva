from django.urls import path
from . import views
from .views import (
    CellarListView,
    CellarDetailView,
    CellarCreateView,
    CellarUpdateView,
    CellarDeleteView,
    InventoryMovementListView,
    InventoryMovementDetailView,
    InventoryMovementCreateView,
    InventoryMovementUpdateView,
    InventoryMovementDeleteView,
)

urlpatterns = [
    path('cellars/', CellarListView.as_view(), name='cellar_list'),
    path('cellars/<int:pk>/', CellarDetailView.as_view(), name='cellar_detail'),
    path('cellars/create/', CellarCreateView.as_view(), name='cellar_create'),
    path('cellars/<int:pk>/update/', CellarUpdateView.as_view(), name='cellar_update'),
    path('cellars/<int:pk>/delete/', CellarDeleteView.as_view(), name='cellar_delete'),
    path('cellars/export/', views.export_cellars_to_excel, name='cellar_export'),

    path('inventory-movements/', InventoryMovementListView.as_view(), name='inventorymovement_list'),
    path('inventory-movements/<int:pk>/', InventoryMovementDetailView.as_view(), name='inventorymovement_detail'),
    path('inventory-movements/create/', InventoryMovementCreateView.as_view(), name='inventorymovement_create'),
    path('inventory-movements/<int:pk>/update/', InventoryMovementUpdateView.as_view(), name='inventorymovement_update'),
    path('inventory-movements/<int:pk>/delete/', InventoryMovementDeleteView.as_view(), name='inventorymovement_delete'),
    path('inventory-movements/export/', views.export_inventory_movements_to_excel, name='inventorymovement_export'),
]