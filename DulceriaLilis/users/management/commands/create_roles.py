from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from users.models import User
from catalog.models import Product
from suppliers.models import Supplier

class Command(BaseCommand):
    help = 'Creates default user groups and assigns permissions.'

    def handle(self, *args, **options):
        # Define roles and their permissions
        roles = {
            'Administrador': {
                'permissions': {
                    User: ['add', 'change', 'delete', 'view'],
                    Product: ['add', 'change', 'delete', 'view'],
                    Supplier: ['add', 'change', 'delete', 'view'],
                }
            },
            'Editor': {
                'permissions': {
                    User: ['view'],
                    Product: ['add', 'change', 'view'],
                    Supplier: ['add', 'change', 'view'],
                }
            },
            'Lector': {
                'permissions': {
                    User: ['view'],
                    Product: ['view'],
                    Supplier: ['view'],
                }
            },
        }

        for role_name, role_data in roles.items():
            group, created = Group.objects.get_or_create(name=role_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created group: {role_name}'))

            # Clear existing permissions for the group before adding new ones
            group.permissions.clear()

            for model, perms in role_data['permissions'].items():
                for perm_codename_action in perms:
                    perm_codename = f'{perm_codename_action}_{model.__name__.lower()}'
                    try:
                        content_type = ContentType.objects.get_for_model(model)
                        permission = Permission.objects.get(content_type=content_type, codename=perm_codename)
                        group.permissions.add(permission)
                        self.stdout.write(self.style.SUCCESS(f'  Added permission {perm_codename} to {role_name}'))
                    except Permission.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f'  Permission {perm_codename} does not exist. Skipping.'))
                    except ContentType.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f'  Content type for {model.__name__} model does not exist. Skipping permission {perm_codename}.'))

        self.stdout.write(self.style.SUCCESS('Default user groups and permissions setup complete.'))
