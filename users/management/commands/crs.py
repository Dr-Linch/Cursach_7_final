from django.core import management
from users.models import User


class Command(management.BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='habit@gmail.com',
            first_name='Nik',
            last_name='Malina',
            is_active=True,
            is_staff=True,
            is_superuser=True
        )
        user.set_password('Linch_21')
        user.save()
