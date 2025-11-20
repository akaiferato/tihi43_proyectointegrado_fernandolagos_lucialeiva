from django.db import models
from django_countries.fields import CountryField


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


class Supplier(Base):
    class stateChoices(models.TextChoices):
        ACTIVO = 'ACT', 'Activo'
        INACTIVO = 'INA', 'Inactivo'
        BLOQUEADO = 'BLQ', 'Bloqueado'

    rut_nif = models.CharField(max_length=20,
                               blank=False,
                               unique=True)
    trade_name = models.CharField(max_length=255,
                                  blank=False)
    company_name = models.CharField(max_length=255,
                                    blank=True)
    email = models.EmailField(blank=False)
    telephone_number = models.CharField(max_length=30,
                                        blank=True)
    website = models.URLField(blank=True)
    direction = models.CharField(max_length=255,
                                 blank=True)
    country = CountryField(default="Chile",
                           blank=False)
    pay_conditions = models.CharField(max_length=255,
                                      blank=False)
    currency = models.CharField(max_length=8,
                                blank=False)
    state = models.CharField(max_length=3,
                             choices=stateChoices.choices)

    def __str__(self):
        return self.trade_name
