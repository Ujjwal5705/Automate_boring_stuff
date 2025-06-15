from django.apps import apps
from django.db.utils import DataError
from django.core.mail import EmailMessage
from django.conf import settings
import csv


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


def send_email_notification(mail_subject, message):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = settings.DEFAULT_TO_EMAIL
        mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
        mail.send()
    except Exception as e:
        raise e