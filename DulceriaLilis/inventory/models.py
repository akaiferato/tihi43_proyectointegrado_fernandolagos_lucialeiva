from django.db import models
from django.utils import timezone
from suppliers.models import Supplier
from catalog.models import Product
from users.models import User

# movimientoInventario, bodega, tipoMovimiento


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Fecha de Creacion")
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name="Ultima Modificacion")
    deleted_at = models.DateTimeField(null=True,
                                      blank=True,
                                      verbose_name="Fecha de Eliminacion")

    class Meta:
        abstract = True


class movementType(Base):
    class movementChoice(models.TextChoices):
        INGRESO = 'IN', 'Ingreso'
        SALIDA = 'OUT', 'Salida'
        AJUSTE = 'ADJ', 'Ajuste'
        DEVOLUCION = 'DEVOL', 'Devolucion'
        TRANSFERENCIA = 'TRANS', 'Transferencia'

    movement_type = models.CharField(max_length=5,
                                     choices=movementChoice.choices)


class Cellar(Base):
    cellar_name = models.CharField(max_length=20,
                                   blank=False)
    location = models.CharField(max_length=255,
                                blank=True)
    
    def __str__(self):
        return self.cellar_name


class inventoryMovement(Base):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    cellar = models.ForeignKey(Cellar,
                               on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier,
                                 on_delete=models.CASCADE)
    movement_type = models.ForeignKey(movementType,
                                      on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(blank=False)
    batch = models.IntegerField(blank=True)
    serie = models.IntegerField(blank=True)
    caducity_date = models.DateField(blank=True)
    observations = models.TextField(blank=True)
