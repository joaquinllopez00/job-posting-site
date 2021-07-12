from mimesis import Person, Text, Address
from django.core.management.base import BaseCommand
from user.models import Category, User, Listing
from django.utils.timezone import now
import random


class Command(BaseCommand):
    help = 'Creates pseudo users w/ listings'

    def handle(self, *args, **options):
        person = Person()
        text = Text()
        address = Address('EN')

        self.stdout.write(f"Creating test user...")

        if not User.objects.filter(username='test'):

            user = User.objects.create_user(
                username='test',
                password='asdf',
                bio=text.text(),
                email=f'{text.word()}@{text.word()}.com',
                role='employer',
                name='ThisIsThe TestUser'
            )

            category = Category.objects.create(
                name=text.word()
            )

            company_name = f'{text.word()}{text.word()}'

            Listing.objects.create(
                    user=user,
                    title=f'I want to hire a {person.occupation()}!',
                    description=text.text(),
                    location=f'{address.address()}, {address.city()}, {address.state()}',
                    job_type=random.randint(1, 3),
                    category=category,
                    salary=random.randint(25000, 150000),
                    company_name=company_name,
                    company_description=text.text(),
                    url=f'https://{company_name}.com',
                    post_date=now()
            )

            self.stdout.write(self.style.SUCCESS("Sucessfully created test user!"))

        else:
            self.stdout.write(self.style.WARNING('Test user already present! Skipping...'))

        self.stdout.write(f"Creating users w/ listings...")
        
        for _ in range(20):

            user = User.objects.create_user(
                username=person.username(),
                password=person.password(),
                bio=text.text(),
                email=f'{text.word()}@{text.word()}.com',
                role='employer',
                name=person.full_name()
            )

            category = Category.objects.create(
                name=text.word()
            )

            company_name = f'{text.word()}{text.word()}'

            for __ in range(2):
                Listing.objects.create(
                    user=user,
                    title=f'I want to hire a {person.occupation()}!',
                    description=text.text(),
                    location=f'{address.address()}, {address.city()}, {address.state()}',
                    job_type=random.randint(1, 3),
                    category=category,
                    salary=random.randint(25000, 150000),
                    company_name=company_name,
                    company_description=text.text(),
                    url=f'https://{company_name}.com',
                    post_date=now()
            )

        self.stdout.write(self.style.SUCCESS("Sucessfully created users w/ listings!"))

        self.stdout.write(f"Creating users...")

        for _ in range(20):

            user = User.objects.create_user(
                username=person.username(),
                password=person.password(),
                bio=text.text(),
                email=f'{text.word()}@{text.word()}.com',
                role='employee',
                name=person.full_name()
            )

        self.stdout.write(self.style.SUCCESS("Sucessfully created users!"))

        self.stdout.write(self.style.SUCCESS("All Done!"))
