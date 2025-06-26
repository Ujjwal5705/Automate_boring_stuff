from django.contrib import admin
from .models import Stock, Stockdata

# Register your models here.

class StockAdmin(admin.ModelAdmin):
    list_display = ['name', 'symbol', 'exchange']

admin.site.register(Stock, StockAdmin)
admin.site.register(Stockdata)