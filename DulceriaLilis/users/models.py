from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class stateChoices(models.TextChoices):
        ACTIVO = 'ACT', 'Activo'
        INACTIVO = 'INA', 'Inactivo'
        BLOQUEADO = 'BLQ', 'Bloqueado'

    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Fecha de Creacion")
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name="Ultima Modificacion")
    deleted_at = models.DateTimeField(null=True,
                                      blank=True,
                                      verbose_name="Fecha de Eliminacion")
    telephone_number = models.CharField(max_length=20,
                                        blank=True)
    state = models.CharField(max_length=3,
                             choices=stateChoices.choices,
                             default='ACT')
    mfa_enabled = models.BooleanField(blank=False,
                                      default=False)
    area = models.CharField(max_length=20,
                            blank=True)
    observaciones = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg', blank=True, null=True)

    groups = models.ManyToManyField('auth.Group',
                                    verbose_name=('groups'),
                                    blank=True,
                                    help_text=(
                                        'The groups this user belongs to. A user will get all permissions '
                                        'granted to each of their groups.'),
                                    related_name="custom_user_groups",
                                    related_query_name="custom_user_group",)
    user_permissions = models.ManyToManyField('auth.Permission',
                                              verbose_name=(
                                                  'user permissions'),
                                              blank=True,
                                              help_text=(
                                                  'Specific permissions for this user.'),
                                              related_name="custom_user_permissions",
                                              related_query_name="custom_user_permission",)
