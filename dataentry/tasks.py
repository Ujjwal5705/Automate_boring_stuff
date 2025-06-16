from awd_main.celery import app
from django.core.management import call_command
from .utils import send_email_notification


@app.task
def import_command(file_path, model_name):
    try:
        call_command('importdata', file_path, model_name)

        # Email after data import succeed
        mail_subject = 'Import Data Completed ✅'
        message = 'Your data has been imported successfully.'
        send_email_notification(mail_subject, message)
        return 'Data imported successfully'
    except Exception as e:
        raise e


@app.task
def export_command(model_name):
    try:
        call_command('exportdata', model_name)

        # Success mail with attachment
        mail_subject = 'Export Data Completed ✅'
        message = 'Your data has been exported successfully.'
        send_email_notification(mail_subject, message)
        return 'Data exported successfully'
    except Exception as e:
        raise e