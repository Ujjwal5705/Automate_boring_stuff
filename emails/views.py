from django.shortcuts import render, redirect
from .forms import EmailForm
from django.contrib import messages
from django.http import HttpResponse
from dataentry.utils import send_email_notification
from .models import Email, Sent
from django.conf import settings
from django.db.models import Sum
from .models import Subscriber, EmailTracking
from .tasks import send_email_task
from django.utils import timezone
import time


# Create your views here.

def send_emails(request):
    if request.method == 'POST':
        email_form = EmailForm(request.POST, request.FILES)
        if email_form.is_valid():
            email = email_form.save()

            # Send bulk email
            mail_subject = request.POST.get('subject')
            message = request.POST.get('body')
            list = request.POST.get('list')
            email_list = Subscriber.objects.filter(list=list)

            if email.attachment:
                attachment = email.attachment.path
            else:
                attachment = None

            email_id = email.id

            to_email = [email.email_address for email in email_list]
            
            # Handover email sending task to celery
            send_email_task.delay(mail_subject, message, to_email, attachment, email_id)
            
            messages.success(request, 'Email sent successfully')
        else:
            messages.error(request, 'Something went wrong! Try again')
        return redirect('send_emails')
    else:
        email = EmailForm()
        context = {'email_form': email}
        return render(request, 'emails/send_emails.html', context)
    

def track_click(request, unique_id):
    try:
        email_tracking = EmailTracking.objects.get(unique_id=unique_id)
        if not email_tracking.clicked_at:
            email_tracking.clicked_at = timezone.now()
            email_tracking.save()
            return redirect(request.GET['url'])
        else:
            print('Link already clicked.')
            return redirect(request.GET['url'])
    except:
        return HttpResponse('Email Record is not found')


def track_open(request, unique_id):
    try:
        email_tracking = EmailTracking.objects.get(unique_id=unique_id)
        if not email_tracking.opened_at:
            delta = timezone.now() - email_tracking.created_at
            if delta.total_seconds() > 10:
                email_tracking.opened_at = timezone.now()
                email_tracking.save()
                return HttpResponse('Email opened successfully.')
            else:
                return HttpResponse('Cached by Sendinblue')
        else:
            print('Email already opened.')
            return HttpResponse('Email already opened.')
    except:
        return HttpResponse('Email Record is not found!')


def track_dashboard(request):
    emails = Email.objects.all().annotate(total_count=Sum('sent__sent_count')).order_by('-sent_at')
    context = {
        'emails': emails,
    }
    return render(request, 'emails/track_dashboard.html', context)


def track_stats(request, pk):
    email = Email.objects.get(id=pk)
    sent = Sent.objects.get(email=email)
    context = {
        'total_count': sent.sent_count,
        'email': email,
    }
    return render(request, 'emails/track_stats.html', context)