from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Supplier
from .forms import SupplierForm
from django.utils.decorators import method_decorator
from users.decorators import group_required

@method_decorator(group_required('Administrador', 'Editor', 'Lector'), name='dispatch')
class SupplierListView(ListView):
    model = Supplier
    template_name = 'suppliers/supplier_list.html'
    context_object_name = 'suppliers'

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