# core/management/commands/populate_dummy_data.py
from django.core.management.base import BaseCommand
from faker import Faker
from core.models import CustomUser, Provider, Menu

fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with dummy data'

    def create_dummy_users(self, num_users=10):
        users = []
        for _ in range(num_users):
            user = CustomUser.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password="dummy_password"
            )
            users.append(user)
        return users

    def create_dummy_providers(self, num_providers=5):
        providers = []
        for _ in range(num_providers):
            user = self.create_dummy_users(1)[0]  # Assign a user to the provider
            name = fake.company()
            bio = fake.text()
            portfolio = fake.url()
            experience = fake.random_int(1, 10)

            # Determine the provider type (Bartender or Chef)
            provider_type = fake.random_element(elements=('Bartender', 'Chef'))
            skills = 'Mixology' if provider_type == 'Bartender' else 'Culinary Arts'

            # Create a Provider instance with the collected data
            provider = Provider.objects.create(
                user=user,
                name=name,
                bio=bio,
                skills=skills,
                portfolio=portfolio,
                experience=experience,
                provider_type=provider_type,
                # Add other fields as needed
            )
            providers.append(provider)
        return providers

    def create_dummy_menus(self, provider, num_menus=3):
        menus = []
        for _ in range(num_menus):
            menu = Menu.objects.create(
                provider=provider,  # Assign a provider to the menu
                title=fake.word(),
                description=fake.sentence(),
                price=fake.random_int(1, 100),
                # Add other fields as needed
            )
            menus.append(menu)
        return menus

    def handle(self, *args, **options):
        # Create dummy users
        users = self.create_dummy_users()

        # Create dummy providers
        providers = self.create_dummy_providers()

        # Create dummy menus for each provider
        for provider in providers:
            self.create_dummy_menus(provider)

        self.stdout.write(self.style.SUCCESS('Dummy data populated successfully.'))
