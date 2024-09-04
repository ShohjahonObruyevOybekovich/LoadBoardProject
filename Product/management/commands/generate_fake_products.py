from django.core.management.base import BaseCommand
from Product.models import Product, CustomUser
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Generate 100 fake products'

    def handle(self, *args, **kwargs):
        fake = Faker()
        user = CustomUser.objects.first()

        if not user:
            self.stdout.write(self.style.ERROR('No users found. Please create a user first.'))
            return

        for _ in range(1000):
            Product.objects.create(
                title=fake.word(),
                places=fake.city(),
                view=fake.sentence(),
                cube=fake.random_number(digits=2),
                kg=fake.random_number(digits=2),
                cube_kg=fake.random_number(digits=2),
                price=fake.random_number(digits=4),
                payment=fake.random_number(digits=4),
                debt=fake.random_number(digits=4),
                where_from=fake.city(),
                date=fake.date_time_this_year(),
                transport=fake.word(),
                current_place=fake.address(),
                status=random.choice(['На складе Китая', 'На складе Узбекистана', 'в пути', 'Ожидающий', 'Завершен']),
                user=user
            )

        self.stdout.write(self.style.SUCCESS('Successfully added 100 fake products'))
