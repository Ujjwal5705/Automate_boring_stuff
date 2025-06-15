from django.db import models

# Create your models here.

class Student(models.Model):
    roll_no = models.CharField(max_length=10)
    name = models.CharField(max_length=20)
    age = models.IntegerField()

    def __str__(self):
        return self.name
    

class Customer(models.Model):
    customer_name = models.CharField(max_length=20)
    country = models.CharField(max_length=20)

    def __str__(self):
        return self.customer_name
    

class Yelp(models.Model):
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    number_review = models.IntegerField()
    category = models.CharField(max_length=20)
    country = models.CharField(max_length=10)
    country_code = models.CharField(max_length=10)
    state = models.CharField(max_length=10)
    city = models.CharField(max_length=20)
    street = models.CharField(max_length=20)
    building = models.CharField(max_length=10)