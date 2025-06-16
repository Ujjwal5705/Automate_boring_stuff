import csv
from django.core.management.base import BaseCommand
from django.apps import apps
from dataentry.utils import generate_csv_file 

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
                model = apps.get_model(app.label, model_name)
                data = model.objects.all()
                
                # Get the file path
                file_path = generate_csv_file(model_name)

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