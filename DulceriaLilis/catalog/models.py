from django.db import models
from django.core.exceptions import ValidationError
from suppliers.models import Supplier
# producto, categoria, marca, m:m productoproveedor


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


class Category(Base):
    name = models.CharField(max_length=20,
                            blank=False)

    def __str__(self):
        return self.name


class Brand(Base):
    name = models.CharField(max_length=20,
                            blank=False)

    def __str__(self):
        return self.name


class Product(Base):
    sku = models.IntegerField(unique=True,
                              blank=False)
    ean_upc = models.CharField(max_length=13,
                               unique=True,
                               blank=True)
    name = models.CharField(max_length=30,
                            blank=False)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,
                              blank=True,
                              on_delete=models.CASCADE)
    supplier = models.ManyToManyField(Supplier)
    model = models.CharField(max_length=30,
                             blank=True)
    uom_purchase = models.CharField(max_length=10,
                                    blank=False)
    uom_sale = models.CharField(max_length=10,
                                blank=False)
    conversion_factor = models.BooleanField(blank=False,
                                            default=True)
    price = models.IntegerField(blank=False)
    iva_tax = models.DecimalField(max_digits=5,
                                  decimal_places=2,
                                  blank=False)
    minimum_stock = models.IntegerField(blank=False,
                                        default=0)
    maximum_stock = models.IntegerField(blank=False)
    perishable = models.BooleanField(blank=False,
                                     default=False)
    batch_control = models.BooleanField(blank=False,
                                        default=False)
    series_control = models.BooleanField(blank=False,
                                         default=False)
    image_url = models.ImageField(blank=True)
    datasheet_url = models.URLField(blank=True)

    def clean(self):
        if self.minimum_stock < 0:
            raise ValidationError("El stock minimo no deberia ser negativo.")

        if self.minimum_stock > self.maximum_stock:
            raise ValidationError(
                "El stock minimo no deberia ser mayor al stock maximo.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class productSupplier(Base):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier,
                                 on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=18,
                               decimal_places=6,
                               blank=False)
    lead_time = models.IntegerField(default=7,
                                    blank=False)
    minimum_batch = models.DecimalField(max_digits=18,
                                        decimal_places=6,
                                        blank=True,
                                        default=1)
    pct_discount = models.DecimalField(max_digits=5,
                                       decimal_places=2,
                                       blank=True)
    preferential = models.BooleanField(blank=False,
                                       default=False)
