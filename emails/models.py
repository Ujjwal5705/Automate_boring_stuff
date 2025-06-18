from django.db import models

# Create your models here.

class List(models.Model):
    list = models.CharField(max_length=25)

    def __str__(self):
        return self.list


class Subscriber(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    email_address = models.EmailField(max_length=50)

    def __str__(self):
        return self.email_address
    

class Email(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    body = models.TextField(max_length=500)
    attachment = models.FileField(blank=True, upload_to='email_attachments/')
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject