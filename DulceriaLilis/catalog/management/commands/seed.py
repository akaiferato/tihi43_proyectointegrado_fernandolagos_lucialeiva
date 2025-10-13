# catalog/management/commands/seed.py

from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting Database Seeding...'))
        call_command('seed_catalog')
        call_command('seed_inventory')
        self.stdout.write(self.style.SUCCESS('Database Seeding Complete!'))
