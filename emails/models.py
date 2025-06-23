from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone

# Create your models here.

class List(models.Model):
    list = models.CharField(max_length=25)

    def __str__(self):
        return self.list
    
    def count_emails(self):
        return Subscriber.objects.filter(list=self).count()


class Subscriber(models .Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    email_address = models.EmailField(max_length=50)

    def __str__(self):
        return str(self.email_address)


class Email(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    body = RichTextField()
    attachment = models.FileField(blank=True, upload_to='email_attachments/')
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
    
    def open_rate(self):
        total_sent = self.list.count_emails()
        opened_count = EmailTracking.objects.filter(email=self, opened_at__isnull=False).count()
        open_rate = (opened_count/total_sent)*100 if total_sent > 0 else 0
        return round(open_rate, 2)
    
    def click_rate(self):
        total_sent = self.list.count_emails()
        clicked_count = EmailTracking.objects.filter(email=self, clicked_at__isnull=False).count()
        click_rate = (clicked_count/total_sent)*100 if total_sent > 0 else 0
        return round(click_rate, 2)


class Sent(models.Model):
    email = models.ForeignKey(Email, on_delete=models.CASCADE, null=True, blank=True)
    sent_count = models.IntegerField()

    def __str__(self):
        return str(self.email) + '-' + str(self.sent_count) + ' emails sent'


class EmailTracking(models.Model):
    email = models.ForeignKey(Email, on_delete=models.CASCADE, null=True, blank=True)
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, null=True, blank=True)
    unique_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    opened_at = models.DateTimeField(null=True, blank=True)
    clicked_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.email.subject)