from django.core.management.base import BaseCommand
from faker import Faker
from bagtrac.models import Data
import random

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        for _ in range(1000):  # Generate 1000 sample data entries
            cage_id = f'T{random.randint(1, 5)}'  # Random 'T1' to 'T5'
            data = {
                'cv': fake.random_int(min=1, max=10),
                'bag_seal_id': fake.uuid4(),
                'cage_id': cage_id,
                'time1': fake.date_time_between(start_date='-1y', end_date='now'),
                'user': fake.name()
            }
            Data.objects.create(**data)
        self.stdout.write(self.style.SUCCESS('Sample data added successfully for 1000 entries'))
