from django.core.management.base import BaseCommand
from django.apps import apps
import csv
from dataentry.utils import check_csv_errors

# Proposed Command : pythonmanage.py importdata file_path model_name

class Command(BaseCommand):
    help = 'Import data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')
        parser.add_argument('model_name', type=str, help='name of model')

    def handle(self, *args, **kwargs):
        #get the file path and model_name from command
        file_path = kwargs['file_path']
        model_name = kwargs['model_name']
        
        # Check errors
        model = check_csv_errors(file_path, model_name)

        if model is None:
            self.stderr.write(f'"{model_name}" model does not exist!')
            
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                model.objects.create(**row)
        self.stdout.write(self.style.SUCCESS('Data Imported from CSV file Successfully!'))