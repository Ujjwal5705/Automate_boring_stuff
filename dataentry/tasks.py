from awd_main.celery import app
from django.core.management import call_command


@app.task
def import_command(file_path, model_name):
    try:
        call_command('importdata', file_path, model_name)
    except Exception as e:
        raise e