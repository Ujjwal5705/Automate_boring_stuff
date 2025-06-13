from django.contrib import admin
from .models import Student, Customer

# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'roll_no', 'age']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'country']


admin.site.register(Student, StudentAdmin)
admin.site.register(Customer, CustomerAdmin)