from django.apps import apps
from django.db.utils import DataError
from django.core.mail import EmailMessage
from django.conf import settings
import pendulum
import csv
import os


def get_all_custom_models():
    default_models = ['LogEntry', 'Permission', 'Group', 'User', 'ContentType', 'Session', 'Upload']
    Custom_models = []
    for model in apps.get_models():
        if model.__name__ not in default_models:
            Custom_models.append(model.__name__)
    return Custom_models
    

def check_csv_errors(file_path, model_name):
    model = None
    for app in apps.get_app_configs():
    #search model in current app
        try:
            model = app.get_model(model_name)
                
            # Getting field names of model
            model_fields = [field.name for field in model._meta.fields]
            model_fields = model_fields[1:]

            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                csv_header = reader.fieldnames
                print(csv_header)
                print(model_fields)
                # Comparing CSV file header with model_fields
                if csv_header != model_fields:
                    raise DataError(f"CSV File does not match with the {model.__name__} table fields")
        except LookupError:
            continue     #Continue if model is not found
    return model


def send_email_notification(mail_subject, message, to_email, attachment=None):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
        if attachment is not None:
            mail.attach_file(attachment)
        mail.send()
    except Exception as e:
        raise e


def generate_csv_file(model_name):
    timestamp = pendulum.now().strftime('%Y-%m-%d-%H-%M-%S')

    # Define csv file name
    export_dir = 'exported_data'
    file_name = f'exported_{model_name}_data_{timestamp}.csv'
    file_path = os.path.join(settings.MEDIA_ROOT, export_dir, file_name)
    return file_path