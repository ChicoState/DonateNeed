from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField

# Create your models here.
class Agencies(models.Model):
  name = models.CharField(max_length=100)
  email = models.EmailField(max_length=50)
  address = models.CharField(max_length=100)
  url = models.URLField(max_length=100)
  phone = PhoneField()

class News_Articles(models.Model):
  #picture = models.ImageField(width_field=100)
  url = models.URLField(max_length=100)
  description = models.CharField(max_length=1000)

class Request_Fulfilled(models.Model):
  fulFilledAmount = models.DecimalField(max_digits=10, decimal_places=2)
  promisedAmount = models.DecimalField(max_digits=10, decimal_places=2)
  promisedArrival = models.DateField(auto_now=False)

class Request_In_Progress(models.Model):
  amount_total = models.DecimalField(max_digits=10, decimal_places=2)
  amount_fulfilled = models.DecimalField(max_digits=10, decimal_places=2)
  is_complete = models.BooleanField(default=False)
  date_requested = models.DateField(auto_now=False)
  request_fulfillment = models.ForeignKey(Request_Fulfilled, on_delete=models.CASCADE)

class Account_Page(models.Model):
  requests_fulfilled = models.ForeignKey(Request_Fulfilled, on_delete=models.CASCADE)
  #picture = models.ImageField(width_field=100)

class Agencies_Page(models.Model):
  causes = models.TextField(max_length=150)
  requests = models.ForeignKey(Request_In_Progress, on_delete=models.CASCADE)

class Cause(models.Model):
  title = models.CharField(max_length=100)
  location = models.CharField(max_length=100)
  news_articles = models.ForeignKey(News_Articles, on_delete=models.CASCADE)
