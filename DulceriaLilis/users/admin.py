from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    def has_module_permission(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return True

        roles = [group.name for group in request.user.groups.all()]

        if 'Bodega' in roles:
            return False

        return super().has_module_permission(request)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False
