from django.core.management.base import BaseCommand


# Propose Command : python manage.py geetings name
# Output : Hi {name}, Good Morning!

# self.stdout.write() : white color text
# self.stderr.write() : red color text
# self.stdout.write(self.style.SUCCESS()) : green color text 
# self.stdout.write(self.style.WARNING()) : yellow color text 


class Command(BaseCommand):
    help = 'Greets the user'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Specifies user name')

    def handle(self, *args, **kwargs):
        name = kwargs['name']
        message = f'Hi {name}, Good Morning!'
        self.stdout.write(message) 