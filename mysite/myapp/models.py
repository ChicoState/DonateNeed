from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from phone_field import PhoneField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


CAUSE_TYPES =(
    ("hurricane", "Hurricanes and Tropical Storms"),
    ("earthquake", "Earthquakes"),
    ("fire", "Fires"),
    ("flood", "Floods"),
    ("tornado", "Tornadoes"),
    ("tsunami", "Tsunamies"),
    ("winter_storm", "Winter and Ice Storms"),

)

class Cause(models.Model):
  title = models.CharField(max_length=100)
  location = models.CharField(max_length=100)
  username = models.CharField(max_length=100, null=True)
  type_of_cause = models.CharField(max_length=100, choices=CAUSE_TYPES, default=None)
  # requests_in_progress = models.ManyToManyField(models.Request_In_Progress)
  def __str__(self):
    return self.title


class News_Articles(models.Model):
  picture = models.URLField(max_length=100, null=True, blank=True)
  url = models.URLField(max_length=100, unique=True)
  title = models.CharField(max_length=100, null=True)
  description = models.CharField(max_length=1000, null=True)
  # cause = models.ManyToManyField(Cause, on_delete=models.SET_NULL, blank=True, null=True)








class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  bio = models.TextField(max_length=500, blank=True)
  picture = models.ImageField(upload_to='media/', default="defaultProfilePic.jpg", null=True, blank=True)
  requests_view_hide_completed = models.BooleanField(default=False)
  def __str__(self):
    return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

class Agencies(models.Model):
  name = models.CharField(max_length=100)
  email = models.EmailField(max_length=50)
  address = models.CharField(max_length=100)
  url = models.URLField(max_length=200)
  phone = PhoneField()
  username = models.CharField(max_length=100, null=True, blank=True, unique=True)
  picture = models.ImageField(upload_to='media/', default="defaultProfilePic.jpg", null=True, blank=True)
  causes = models.ManyToManyField(Cause, blank=True)
  admin_users = models.ManyToManyField(User, blank=True, related_name="agency")
  def __str__(self):
      return self.name

# class Agencies_Page(models.Model):
#   # causes = models.ManyToManyField(Cause)
#   agency = models.ForeignKey(Agencies, on_delete=models.CASCADE, null=True, blank=True, unique=True)




class Request_In_Progress(models.Model):
  item = models.CharField(max_length=250, null=True)
  amount_total = models.DecimalField(max_digits=10, decimal_places=0)
  amount_fulfilled = models.DecimalField(max_digits=10, decimal_places=2, default=0)
  is_complete = models.BooleanField(default=False)
  date_requested = models.DateField(auto_now=False, auto_now_add=True)
  agency = models.ForeignKey(Agencies, on_delete=models.SET_NULL, blank=True, null=True)
  cause = models.ForeignKey(Cause, on_delete=models.SET_NULL, blank=True, null=True)
  percent_complete = models.DecimalField(max_digits=10, decimal_places=2, default=0)




class Request_Fulfilled(models.Model):
  fulfilled_amount = models.DecimalField(max_digits=10, decimal_places=0)
  promised_amount = models.DecimalField(max_digits=10, decimal_places=0)
  promised_arrival = models.DateField(auto_now=False)
  user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
  request_in_progress = models.ForeignKey(Request_In_Progress, on_delete=models.CASCADE, blank=True, null=True)
  date = models.DateField(auto_now=True)
