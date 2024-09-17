from django.core.management.base import BaseCommand

from users.models import CustomUser

# Command to make a user an admin
class Command(BaseCommand):
    help = 'Make a user an admin'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='User email')

    def handle(self, *args, **kwargs):
        email = kwargs['email']
        try:
            user = CustomUser.objects.get(email=email)
            if user.profile.rol == 'user':
                user.profile.rol = 'admin'

            user.profile.save()
            self.stdout.write(self.style.SUCCESS(f'{email} is now an admin'))
        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User with email {email} does not exist'))
