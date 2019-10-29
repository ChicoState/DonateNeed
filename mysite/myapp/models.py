from django.db import models
from django.contrib.auth.models import User
#from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Agencies(models.Model):
  name = models.CharField(max_length=100)
  email = models.EmailField(max_length=50)
  address = models.CharField(max_length=100)
  url = models.URLField(max_length=100)
  #phone = models.PhoneNumberField()

class Account_Page(models.Model):
  requests_fulfilled = models.CharField(max_length=100)
  #picture = models.ImageField(width_field=100)

class Agencies_Page(models.Model):
    causes = models.TextField(max_length=150)
  #requests =

class Cause(models.Model):
  title = models.CharField(max_length=100)
  location = models.CharField(max_length=100)
  #news_articles =

class Request_In_Progress(models.Model):
  amount_total = models.DecimalField(max_digits=10, decimal_places=2)
  amount_fulfilled = models.DecimalField(max_digits=10, decimal_places=2)
  is_complete = models.BooleanField(default=False)
  date_requested = models.DateField(auto_now=False)

class News_Articles(models.Model):
  #picture = models.ImageField(width_field=100)
  url = models.URLField(max_length=100)
  description = models.CharField(max_length=1000)


class Request_Fulfilled(models.Model):
  fulFilledAmount = models.DecimalField(max_digits=10, decimal_places=2)
  promisedAmount = models.DecimalField(max_digits=10, decimal_places=2)
  promisedArrival = models.DateField(auto_now=False)
