from rest_framework import routers
from django.urls import path, include
from .views import  UserViewSet, SupplierViewSet

router = routers.DefaultRouter()
router.register(r'usuarios', UserViewSet)
router.register(r'distribuidores', SupplierViewSet)

urlpatterns = [
    path('', include(router.urls))
]
