from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Cellar, inventoryMovement
from .forms import CellarForm, InventoryMovementForm
from django.utils.decorators import method_decorator
from users.decorators import group_required
from django.http import HttpResponse
import openpyxl
from django.db.models import Q

@method_decorator(group_required('Administrador', 'Editor', 'Lector'), name='dispatch')
class CellarListView(ListView):
    model = Cellar
    template_name = 'inventory/cellar_list.html'
    context_object_name = 'cellars'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(cellar_name__icontains=query) |
                Q(location__icontains=query)
            )
        
        sort_by = self.request.GET.get('sort_by', 'cellar_name')
        direction = self.request.GET.get('direction', 'asc')
        if direction == 'desc':
            sort_by = f'-{sort_by}'
        
        return queryset.order_by(sort_by)

    def get_paginate_by(self, queryset):
        paginate_by = self.request.GET.get('paginate_by', self.request.session.get('paginate_by', 10))
        self.request.session['paginate_by'] = paginate_by
        return paginate_by

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paginate_by'] = int(self.get_paginate_by(self.get_queryset()))
        context['sort_by'] = self.request.GET.get('sort_by', 'cellar_name')
        context['direction'] = self.request.GET.get('direction', 'asc')
        return context

@method_decorator(group_required('Administrador', 'Editor', 'Lector'), name='dispatch')
class CellarDetailView(DetailView):
    model = Cellar
    template_name = 'inventory/cellar_detail.html'
    context_object_name = 'cellar'

@method_decorator(group_required('Administrador', 'Editor'), name='dispatch')
class CellarCreateView(CreateView):
    model = Cellar
    form_class = CellarForm
    template_name = 'inventory/cellar_form.html'
    success_url = reverse_lazy('cellar_list')

@method_decorator(group_required('Administrador', 'Editor'), name='dispatch')
class CellarUpdateView(UpdateView):
    model = Cellar
    form_class = CellarForm
    template_name = 'inventory/cellar_form.html'
    success_url = reverse_lazy('cellar_list')

@method_decorator(group_required('Administrador'), name='dispatch')
class CellarDeleteView(DeleteView):
    model = Cellar
    template_name = 'inventory/cellar_confirm_delete.html'
    success_url = reverse_lazy('cellar_list')

@group_required('Administrador', 'Editor', 'Lector')
def export_cellars_to_excel(request):
    cellars = Cellar.objects.all()
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Cellars"

    headers = ["Name", "Location", "Created At", "Updated At"]
    ws.append(headers)

    for cellar in cellars:
        ws.append([
            cellar.cellar_name,
            cellar.location,
            cellar.created_at.strftime("%Y-%m-%d %H:%M:%S") if cellar.created_at else '',
            cellar.updated_at.strftime("%Y-%m-%d %H:%M:%S") if cellar.updated_at else ''
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=cellars.xlsx'
    wb.save(response)

    return response


@method_decorator(group_required('Administrador', 'Editor', 'Lector'), name='dispatch')
class InventoryMovementListView(ListView):
    model = inventoryMovement
    template_name = 'inventory/inventorymovement_list.html'
    context_object_name = 'inventory_movements'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(product__name__icontains=query) |
                Q(cellar__cellar_name__icontains=query) |
                Q(user__username__icontains=query)
            )
        
        sort_by = self.request.GET.get('sort_by', '-created_at')
        direction = self.request.GET.get('direction', 'asc')
        if direction == 'desc':
            sort_by = f'-{sort_by}'
        
        return queryset.order_by(sort_by)

    def get_paginate_by(self, queryset):
        paginate_by = self.request.GET.get('paginate_by', self.request.session.get('paginate_by', 10))
        self.request.session['paginate_by'] = paginate_by
        return paginate_by

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paginate_by'] = int(self.get_paginate_by(self.get_queryset()))
        context['sort_by'] = self.request.GET.get('sort_by', '-created_at')
        context['direction'] = self.request.GET.get('direction', 'asc')
        return context

@method_decorator(group_required('Administrador', 'Editor', 'Lector'), name='dispatch')
class InventoryMovementDetailView(DetailView):
    model = inventoryMovement
    template_name = 'inventory/inventorymovement_detail.html'
    context_object_name = 'inventory_movement'

@method_decorator(group_required('Administrador', 'Editor'), name='dispatch')
class InventoryMovementCreateView(CreateView):
    model = inventoryMovement
    form_class = InventoryMovementForm
    template_name = 'inventory/inventorymovement_form.html'
    success_url = reverse_lazy('inventorymovement_list')

@method_decorator(group_required('Administrador', 'Editor'), name='dispatch')
class InventoryMovementUpdateView(UpdateView):
    model = inventoryMovement
    form_class = InventoryMovementForm
    template_name = 'inventory/inventorymovement_form.html'
    success_url = reverse_lazy('inventorymovement_list')

@method_decorator(group_required('Administrador'), name='dispatch')
class InventoryMovementDeleteView(DeleteView):
    model = inventoryMovement
    template_name = 'inventory/inventorymovement_confirm_delete.html'
    success_url = reverse_lazy('inventorymovement_list')

@group_required('Administrador', 'Editor', 'Lector')
def export_inventory_movements_to_excel(request):
    movements = inventoryMovement.objects.all()
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Inventory Movements"

    headers = ["Product", "Cellar", "User", "Movement Type", "Quantity", "Date"]
    ws.append(headers)

    for movement in movements:
        ws.append([
            movement.product.name,
            movement.cellar.cellar_name,
            movement.user.username,
            movement.get_movement_type_display(),
            movement.quantity,
            movement.created_at.strftime("%Y-%m-%d %H:%M:%S") if movement.created_at else ''
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=inventory_movements.xlsx'
    wb.save(response)

    return response

