from rest_framework import viewsets
from users.models import User
from .serializers import UserSerializer
from suppliers.models import Supplier
from .serializers import SupplierSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.object.all()
    serializer_class = UserSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.object.all()
    serializer_class = SupplierSerializer

