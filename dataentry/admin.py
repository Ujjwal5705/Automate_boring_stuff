from django.contrib import admin
from .models import Student, Customer, Yelp

# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'roll_no', 'age']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'country']

class YelpAdmin(admin.ModelAdmin):
    list_display = ['rating', 'number_review', 'category', 'country', 'country_code', 'state', 'city', 'street', 'building']
    actions = None

admin.site.register(Student, StudentAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Yelp)