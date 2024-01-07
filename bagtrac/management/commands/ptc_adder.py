# Import necessary modules
import os
import csv
from django.core.management.base import BaseCommand
from bagtrac.models import PTC
from django.conf import settings

# Define a Django management command
class Command(BaseCommand):
    help = 'Import data from CSV to PTC model'

    def handle(self, *args, **kwargs):
        static_path = os.path.join(settings.BASE_DIR, 'static')
        file_name = 'ptc.csv'  # Update with your CSV file name
        
        file_path = os.path.join(static_path, file_name)
        
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                grid = row['grid']
                ptc_value = row['ptc']
                
                ptc_obj, created = PTC.objects.get_or_create(grid=grid, defaults={'ptc': ptc_value})
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created PTC entry for grid: {grid}"))
                else:
                    self.stdout.write(self.style.NOTICE(f"PTC entry for grid: {grid} already exists"))
