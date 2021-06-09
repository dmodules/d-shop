from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection


class Command(BaseCommand):

    def handle(self, **options): # noqa
        # Empty DB
        print("Cleaning DB")
        with connection.cursor() as cursor:
            cursor.execute("DROP SCHEMA public CASCADE;")
            cursor.execute("CREATE SCHEMA public;")

        # Migrate DB
        print("Migrating db")
        call_command('migrate')

        # Import data
        print("Importing data")
        call_command('loaddata', 'data.json')
