from django.apps import apps
from django.db.utils import DataError
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings
from emails.models import Email, Sent, Subscriber, EmailTracking
from bs4 import BeautifulSoup
import pendulum
import hashlib
import time
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


def send_email_notification(mail_subject, message, to_email, attachment=None, email_id=None):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        new_message = message
        for email_address in to_email:
            new_message = message
            # Create Email Tracking Record
            if email_id:
                email = Email.objects.get(pk=email_id)
                subscriber = Subscriber.objects.get(list=email.list, email_address=email_address)
                time_stamp = str(time.time())
                date_to_hash = f'{time_stamp}'
                unique_id = hashlib.sha256(date_to_hash.encode()).hexdigest()
                
                try:
                    email_tracking = EmailTracking.objects.create(
                        email = email,
                        subscriber = subscriber,
                        unique_id = unique_id,
                    )
                except Exception as e:
                    raise e

                # Generate the click tracking pixel url
                base_url = settings.BASE_URL
                click_tracking_url = f"{base_url}/emails/track/click/{unique_id}"
                open_tracking_url = f"{base_url}/emails/track/open/{unique_id}/"
                
                # Search for the links in the email body
                soup = BeautifulSoup(email.body, 'html.parser')
                urls = [link.get('href') for link in soup.find_all('a')]

                # If there are urls or links in email body, inject our click_tracking_url to that original link
                if urls:
                    for url in urls:
                        tracking_url = f"{click_tracking_url}?url={url}"
                        new_message = new_message.replace(f'{url}', f'{tracking_url}')

                open_tracking_img = f'<img src="{open_tracking_url}" width="1" height="1">'
                new_message += open_tracking_img

            text_message = strip_tags(new_message)
            mail = EmailMultiAlternatives(
                subject=mail_subject,
                body=text_message,
                from_email=from_email,
                to=[email_address],
            )
            mail.attach_alternative(new_message, "text/html")
            if attachment is not None:
                mail.attach_file(attachment)
            mail.send()
        
        # Store total sent emails in Sent model
        if email_id:
            email = Email.objects.get(pk=email_id)
            sent = Sent()
            sent.email = email
            sent.sent_count = email.list.count_emails()
            sent.save()
    except Exception as e:
        raise e


def generate_csv_file(model_name):
    timestamp = pendulum.now().strftime('%Y-%m-%d-%H-%M-%S')

    # Define csv file name
    export_dir = 'exported_data'
    file_name = f'exported_{model_name}_data_{timestamp}.csv'
    file_path = os.path.join(settings.MEDIA_ROOT, export_dir, file_name)
    return file_path