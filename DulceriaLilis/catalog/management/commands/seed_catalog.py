# catalog/management/commands/seed_catalog.py

from django.core.management.base import BaseCommand
from ._private import create_categories, create_brands, create_suppliers, create_products


class Command(BaseCommand):
    help = 'Seeds the database with catalog data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Seeding Catalog Data...'))
        create_categories()
        create_brands()
        create_suppliers()
        create_products()
        self.stdout.write(self.style.SUCCESS('Catalog Data Seeding Complete!'))
