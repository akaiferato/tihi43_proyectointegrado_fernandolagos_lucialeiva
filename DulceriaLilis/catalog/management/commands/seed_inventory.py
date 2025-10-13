# catalog/management/commands/seed_inventory.py

from django.core.management.base import BaseCommand
from ._private import create_inventory_movements


class Command(BaseCommand):
    help = 'Seeds the database with inventory data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Seeding Inventory Data...'))
        create_inventory_movements()
        self.stdout.write(self.style.SUCCESS(
            'Inventory Data Seeding Complete!'))
