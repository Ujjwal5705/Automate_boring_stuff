from django.shortcuts import render, redirect
from .forms import EmailForm
from django.contrib import messages
from dataentry.utils import send_email_notification
from django.conf import settings
from .models import Subscriber
from .tasks import send_email_task


# Create your views here.


def send_emails(request):
    if request.method == 'POST':
        email_form = EmailForm(request.POST, request.FILES)
        if email_form.is_valid():
            email_form = email_form.save()

            # Send bulk email
            mail_subject = request.POST.get('subject')
            message = request.POST.get('body')
            list = request.POST.get('list')
            email_list = Subscriber.objects.filter(list=list)

            if email_form.attachment:
                attachment = email_form.attachment.path
            else:
                attachment = None

            # Handover email sending task to celery
            for email in email_list:
                to_email = email.email_address
                send_email_task.delay(mail_subject, message, to_email, attachment)
            
            messages.success(request, 'Email sent successfully')
        else:
            messages.error(request, 'Something went wrong! Try again')
        return redirect('send_emails')
    else:
        email_form = EmailForm()
        context = {'email_form': email_form}
        return render(request, 'emails/send_emails.html', context)