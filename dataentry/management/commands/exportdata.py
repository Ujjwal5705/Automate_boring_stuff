import csv
from django.core.management.base import BaseCommand
from django.apps import apps
import pendulum

# Command : python manage.py exportdata model_name

class Command(BaseCommand):
    help = 'Export data to CSV file'

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='name of model')

    def handle(self, *args, **kwargs):
        model_name = kwargs['model_name']
        
        model = None
        for app in apps.get_app_configs():
            try:
                model = app.get_model(model_name)
                data = model.objects.all()
                timestamp = pendulum.now().strftime('%Y-%m-%d-%H-%M-%S')
                # Define csv file name
                file_path = f'exported_{model.__name__}_data_{timestamp}.csv'

                with open(file_path, 'w', newline='') as file:
                    writer = csv.writer(file)

                    # write header of data in csv file
                    writer.writerow([field.name for field in model._meta.fields])

                    # write data
                    for dt in data:
                        writer.writerow([getattr(dt, field.name) for field in model._meta.fields])

                    self.stdout.write(self.style.SUCCESS('Data exported Successfully'))
            except LookupError:
                continue
        
        if model is None:
            self.stderr.write(f'"{model_name}" model does not exists!')