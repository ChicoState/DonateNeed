from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from phone_field import PhoneField
from django.conf import settings
from django.db.models.signals import post_save
# from django.dispatch import receiver

# Create your models here.
class Agencies(models.Model):
  name = models.CharField(max_length=100)
  email = models.EmailField(max_length=50)
  address = models.CharField(max_length=100)
  url = models.URLField(max_length=100)
  phone = PhoneField()
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.SET_NULL, blank=True, null=True)


class News_Articles(models.Model):
  picture = models.ImageField(width_field=100, default="media/redCross.jpg")
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
  request_fulfillment = models.ForeignKey(Request_Fulfilled, on_delete=models.CASCADE, blank=True, null=True)

class Account_Page(models.Model):
  requests_fulfilled = models.ForeignKey(Request_Fulfilled, on_delete=models.CASCADE, blank=True, null=True)
  picture = models.ImageField(width_field=100, default="media/redCross.jpg")

class Agencies_Page(models.Model):
  causes = models.TextField(max_length=150)
  requests = models.ForeignKey(Request_In_Progress, on_delete=models.CASCADE, blank=True, null=True)

class Cause(models.Model):
  title = models.CharField(max_length=100)
  location = models.CharField(max_length=100)
  news_articles = models.ForeignKey(News_Articles, on_delete=models.CASCADE, blank=True, null=True)

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  bio = models.TextField(max_length=500, blank=True)
  agencies = models.ForeignKey(Agencies, on_delete=models.SET_NULL, blank=True, null=True)
  #picture = models.ImageField(width_field=100, default="media/defaultProfilePic.jpg")

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
