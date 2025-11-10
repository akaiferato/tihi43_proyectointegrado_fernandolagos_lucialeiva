from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Supplier
from .forms import SupplierForm
from django.utils.decorators import method_decorator
from users.decorators import group_required
from django.http import HttpResponse
import openpyxl
from django.db.models import Q

@method_decorator(group_required('Administrador', 'Editor', 'Lector'), name='dispatch')
class SupplierListView(ListView):
    model = Supplier
    template_name = 'suppliers/supplier_list.html'
    context_object_name = 'suppliers'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(trade_name__icontains=query) |
                Q(company_name__icontains=query) |
                Q(email__icontains=query)
            )
        
        sort_by = self.request.GET.get('sort_by', 'trade_name')
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
        context['sort_by'] = self.request.GET.get('sort_by', 'trade_name')
        context['direction'] = self.request.GET.get('direction', 'asc')
        return context

@method_decorator(group_required('Administrador', 'Editor', 'Lector'), name='dispatch')
class SupplierDetailView(DetailView):
    model = Supplier
    template_name = 'suppliers/supplier_detail.html'
    context_object_name = 'supplier'

@method_decorator(group_required('Administrador', 'Editor'), name='dispatch')
class SupplierCreateView(CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/supplier_form.html'
    success_url = reverse_lazy('supplier_list')

@method_decorator(group_required('Administrador', 'Editor'), name='dispatch')
class SupplierUpdateView(UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/supplier_form.html'
    success_url = reverse_lazy('supplier_list')

@method_decorator(group_required('Administrador'), name='dispatch')
class SupplierDeleteView(DeleteView):
    model = Supplier
    template_name = 'suppliers/supplier_confirm_delete.html'
    success_url = reverse_lazy('supplier_list')

@group_required('Administrador', 'Editor', 'Lector')
def export_suppliers_to_excel(request):
    suppliers = Supplier.objects.all()
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Suppliers"

    headers = ["RUT/NIF", "Trade Name", "Company Name", "Email", "Phone", "Direction", "Country"]
    ws.append(headers)

    for supplier in suppliers:
        ws.append([supplier.rut_nif, supplier.trade_name, supplier.company_name, supplier.email, supplier.telephone_number, supplier.direction, supplier.country.name])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=suppliers.xlsx'
    wb.save(response)

    return response