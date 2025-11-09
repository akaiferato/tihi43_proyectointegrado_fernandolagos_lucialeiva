from django.urls import path
from .views import (
    SupplierListView,
    SupplierDetailView,
    SupplierCreateView,
    SupplierUpdateView,
    SupplierDeleteView,
)

urlpatterns = [
    path('suppliers/', SupplierListView.as_view(), name='supplier_list'),
    path('suppliers/<int:pk>/', SupplierDetailView.as_view(), name='supplier_detail'),
    path('suppliers/create/', SupplierCreateView.as_view(), name='supplier_create'),
    path('suppliers/<int:pk>/update/', SupplierUpdateView.as_view(), name='supplier_update'),
    path('suppliers/<int:pk>/delete/', SupplierDeleteView.as_view(), name='supplier_delete'),
]
