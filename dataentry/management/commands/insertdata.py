from django.core.management.base import BaseCommand
from dataentry.models import Student

# I want to add some data to the database using the custom command

class Command(BaseCommand):
    help = 'it will insert data to the database'

    def handle(self, *args, **kwargs):
        #logic
        datasets = [
            {'roll_no': 1001, 'name': 'Ujjwal', 'age': 21},
            {'roll_no': 1002, 'name': 'John', 'age': 22},
            {'roll_no': 1003, 'name': 'Mike', 'age': 23},
        ]

        for data in datasets:
            existing_record = Student.objects.filter(roll_no = data['roll_no']).exists()

            if not existing_record:
                Student.objects.create(roll_no = data['roll_no'], name = data['name'], age = data['age'])
            else:
                self.stdout.write(self.style.WARNING(f'Student with Roll No. {data['roll_no']} already exists!'))
        self.stdout.write(self.style.SUCCESS('Data inserted Successfully!'))