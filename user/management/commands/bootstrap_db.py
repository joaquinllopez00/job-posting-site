from mimesis import Person, Text
from django.core.management.base import BaseCommand
from user.models import User
from job.models import Listing


class Command(BaseCommand):
    help = 'Creates pseudo users w/ listings'

    def handle(self, *args, **options):
        person = Person()
        text = Text()

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

            Listing.objects.create(
                    creator=user,
                    title=f'I want to hire a {person.occupation()}!',
                    description=text.text()
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

            for __ in range(2):
                Listing.objects.create(
                    creator=user,
                    title=f'I want to hire a {person.occupation()}!',
                    description=text.text()
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
