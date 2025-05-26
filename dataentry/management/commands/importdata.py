from django.core.management.base import BaseCommand
from dataentry.models import Student
from django.apps import apps
import csv

# Proposed Command : pythonmanage.py importdata file_path

class Command(BaseCommand):
    help = 'Import data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')
        parser.add_argument('model_name', type=str, help='name of model')

    def handle(self, *args, **kwargs):
        #get the file path and model_name from command
        file_path = kwargs['file_path']
        model_name = kwargs['model_name']
        
        model = None
        for app in apps.get_app_configs():
            #search model in current app
            try:
                model = app.get_model(model_name)
                with open(file_path, 'r') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        model.objects.create(**row)
                self.stdout.write(self.style.SUCCESS('Data Imported from CSV file Successfully!'))
                break   #Once model is found, import the data and break the loop
            except LookupError:
                continue #Continue if model is not found

        if model is None:
            self.stderr.write(f'"{model_name}" model does not exist!')