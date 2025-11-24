from rest_framework import routers
from django.urls import path, include
from .views import  UserViewSet, SupplierViewSet, CategoryViewSet, BrandViewSet

router = routers.DefaultRouter()
router.register(r'usuarios', UserViewSet)
router.register(r'distribuidores', SupplierViewSet)
router.register(r'categorias', CategoryViewSet)
router.register(r'marcas', BrandViewSet)

urlpatterns = [
    path('', include(router.urls))
]
