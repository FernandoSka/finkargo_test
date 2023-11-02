from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Command to verify is the user admin exits, case don't create it"""

    def handle(self, *args, **options):
        user_admin = get_user_model().objects.filter(email="master@master.com")
        if len(user_admin) == 0:
            self.stdout.write('Admin User not exits, will be creating automatically')
            payload = {
                'email': "master@master.com",
                'password': "123abc456",
                'name': 'Master Administrator',
                'last_name': 'Admin',
            }
            user_admin = get_user_model().objects.create_user(**payload)
            if user_admin is None:
                self.stdout.write(self.style.ERROR('An error ocurring at create admin user!!!!!!!'))
            else:
                self.stdout.write(self.style.SUCCESS('Admin User created'))
