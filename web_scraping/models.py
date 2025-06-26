from django.db import models

# Create your models here.

class Stock(models.Model):
    symbol = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    exchange = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Stockdata(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    current_price = models.CharField(max_length=50, null=True, blank=True)
    price_change = models.CharField(max_length=50, null=True, blank=True)
    percent_change = models.CharField(max_length=50, null=True, blank=True)
    previous_close = models.CharField(max_length=50, null=True, blank=True)
    week_52_high = models.CharField(max_length=50, null=True, blank=True)
    week_52_low = models.CharField(max_length=50, null=True, blank=True)
    market_cap = models.CharField(max_length=50, null=True, blank=True)
    pe_ratio = models.CharField(max_length=50, null=True, blank=True)
    dividend_yield = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.stock.name}" '-' f"{self.current_price}"