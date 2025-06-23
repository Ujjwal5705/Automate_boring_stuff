from awd_main.celery import app
from django.core.management import call_command
from .utils import send_email_notification, generate_csv_file
from django.conf import settings

@app.task
def import_command(file_path, model_name):
    try:
        call_command('importdata', file_path, model_name)

        # Email after data import succeed
        mail_subject = 'Import Data Completed ✅'
        message = 'Your data has been imported successfully.'
        to_email = settings.DEFAULT_TO_EMAIL
        send_email_notification(mail_subject, message, [to_email])
        return 'Data imported successfully'
    except Exception as e:
        raise e


@app.task
def export_command(model_name):
    try:
        call_command('exportdata', model_name)

        file_path = generate_csv_file(model_name)

        # Success mail with attachment
        mail_subject = 'Export Data Completed ✅'
        message = 'Your data has been exported successfully.'
        to_email = settings.DEFAULT_TO_EMAIL
        send_email_notification(mail_subject, message, [to_email], attachment=file_path)
        return 'Data exported successfully'
    except Exception as e:
        raise e