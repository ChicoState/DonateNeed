from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from phone_field import PhoneField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Cause(models.Model):
  title = models.CharField(max_length=100)
  location = models.CharField(max_length=100)
  username = models.CharField(max_length=100, null=True)
  def __str__(self):
    return self.title


class News_Articles(models.Model):
  picture = models.URLField(max_length=100, null=True)
  url = models.URLField(max_length=100)
  title = models.CharField(max_length=100, null=True)
  description = models.CharField(max_length=1000, null=True)
  # cause = models.ManyToManyField(Cause, on_delete=models.SET_NULL, blank=True, null=True)




class Agencies(models.Model):
  name = models.CharField(max_length=100)
  email = models.EmailField(max_length=50)
  address = models.CharField(max_length=100)
  url = models.URLField(max_length=200)
  phone = PhoneField()
  username = models.CharField(max_length=100, null=True)
  picture = models.ImageField(upload_to='media/', default="defaultProfilePic.jpg", null=True, blank=True)
  causes = models.ManyToManyField(Cause, blank=True)
  def __str__(self):
      return self.name



class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  bio = models.TextField(max_length=500, blank=True)
  agencies = models.ForeignKey(Agencies, on_delete=models.SET_NULL, blank=True, null=True)
  picture = models.ImageField(upload_to='media/', default="defaultProfilePic.jpg", null=True, blank=True)

  def __str__(self):
    return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)



# class Agencies_Page(models.Model):
#   # causes = models.ManyToManyField(Cause)
#   agency = models.ForeignKey(Agencies, on_delete=models.CASCADE, null=True, blank=True, unique=True)




class Request_In_Progress(models.Model):
  item = models.CharField(max_length=250)
  amount_total = models.DecimalField(max_digits=10, decimal_places=2)
  amount_fulfilled = models.DecimalField(max_digits=10, decimal_places=2, default=0)
  is_complete = models.BooleanField(default=False)
  date_requested = models.DateField(auto_now=False)
  agency = models.ForeignKey(Agencies, on_delete=models.SET_NULL, blank=True, null=True)



class Request_Fulfilled(models.Model):
  fulfilled_amount = models.DecimalField(max_digits=10, decimal_places=2)
  promised_amount = models.DecimalField(max_digits=10, decimal_places=2)
  promised_arrival = models.DateField(auto_now=False)
  user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
  request_in_progress = models.ForeignKey(Request_In_Progress, on_delete=models.CASCADE, blank=True, null=True)
