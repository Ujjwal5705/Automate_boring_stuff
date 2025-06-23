from django.contrib import admin
from .models import List, Subscriber, Email, EmailTracking, Sent

# Register your models here.

class EmailTrackingAdmin(admin.ModelAdmin):
    list_display = ['subscriber', 'unique_id', 'created_at', 'opened_at', 'clicked_at']

admin.site.register(List)
admin.site.register(Subscriber)
admin.site.register(Email)
admin.site.register(EmailTracking, EmailTrackingAdmin)
admin.site.register(Sent)