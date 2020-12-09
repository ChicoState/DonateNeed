from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from phone_field import PhoneField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from cities_light.models import City


CAUSE_TYPES =(
    ("hurricane", "Hurricanes and Tropical Storms"),
    ("earthquake", "Earthquakes"),
    ("fire", "Fires"),
    ("flood", "Floods"),
    ("tornado", "Tornadoes"),
    ("tsunami", "Tsunamies"),
    ("winter_storm", "Winter and Ice Storms"),
    ("general", "General Organization Request")

)

class Cause(models.Model):
  title = models.CharField(max_length=100)
  location = models.ForeignKey(City, on_delete=models.PROTECT, default=None) #models.CharField(max_length=100)
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


class Agencies(models.Model):
  name = models.CharField(max_length=100)
  email = models.EmailField(max_length=50)
  address = models.CharField(max_length=100)
  url = models.URLField(max_length=200)
  phone = PhoneField()
  city = models.ForeignKey(City, on_delete=models.PROTECT) #models.CharField(max_length=100)
  username = models.CharField(max_length=100, null=True, blank=True, unique=True)
  picture = models.ImageField(upload_to='media/', default="defaultProfilePic.jpg", null=True, blank=True)
  causes = models.ManyToManyField(Cause, blank=True)
  admin_users = models.ManyToManyField(User, blank=True, related_name="agency")
  only_volunteer = models.BooleanField(default=False)
  def __str__(self):
      return self.name


class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  city = models.ForeignKey(City, on_delete=models.PROTECT, null=True, blank=True)
  bio = models.TextField(max_length=500, blank=True)
  picture = models.ImageField(upload_to='media/', default="defaultProfilePic.jpg", null=True, blank=True)
  requests_view_hide_completed = models.BooleanField(default=False)
  number_of_donations = models.DecimalField(max_digits=1000000000000, decimal_places=0, default=0)
  number_of_volunteering_participations = models.DecimalField(max_digits=1000000000000, decimal_places=0, default=0)
  followers = models.ManyToManyField("self", blank=True)
  following = models.ManyToManyField("self", blank=True)
  agencies_following = models.ManyToManyField(Agencies, blank=True, related_name="user_followers")
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

class Volunteering(models.Model):
    number_of_volunteers = models.DecimalField(max_digits=10, decimal_places=0)
    date_needed = models.DateField(auto_now=False, auto_now_add=True)
    location = models.ForeignKey(City, on_delete=models.PROTECT, blank=True, null=True)
    agency = models.ForeignKey(Agencies, on_delete=models.SET_NULL, blank=True, null=True)
    cause = models.ForeignKey(Cause, on_delete=models.SET_NULL, blank=True, null=True, related_name='cs2')
    address = models.CharField(max_length=100, blank=True, null=True)
    amount_fulfilled = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    percent_complete = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    volunteers = models.ManyToManyField(User, blank=True, related_name="volunteer")

SIZES =(
    ("xxxs", "XXXS"),
    ("xxs", "XXS"),
    ("xs", "XS"),
    ("s", "S"),
    ("m", "M"),
    ("l", "L"),
    ("xl", "XL"),
    ("xxl", "2X"),
    ("xxxl", "3X"),
    ("xxxxl", "4X"),

)


class Request_In_Progress(models.Model):
  item = models.CharField(max_length=250, null=True)
  amount_total = models.DecimalField(max_digits=10, decimal_places=0)
  size = models.CharField(max_length=100, choices=SIZES, blank=True)
  amount_fulfilled = models.DecimalField(max_digits=10, decimal_places=2, default=0)
  is_complete = models.BooleanField(default=False)
  date_requested = models.DateField(auto_now=False, auto_now_add=True)
  agency = models.ForeignKey(Agencies, on_delete=models.SET_NULL, blank=True, null=True)
  cause = models.ForeignKey(Cause, on_delete=models.SET_NULL, blank=True, null=True, related_name='cs')
  percent_complete = models.DecimalField(max_digits=10, decimal_places=2, default=0)




class Request_Fulfilled(models.Model):
  fulfilled_amount = models.DecimalField(max_digits=10, decimal_places=0)
  promised_amount = models.DecimalField(max_digits=10, decimal_places=0)
  promised_arrival = models.DateField(auto_now=False)
  user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
  request_in_progress = models.ForeignKey(Request_In_Progress, on_delete=models.CASCADE, blank=True, null=True)
  date = models.DateField(auto_now=True)



class Social_Media_Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=10000, null=True)
    agency_profile = models.CharField(max_length=10000, null=True)
    agency_name = models.CharField(max_length=10000, null=True)
    date_posted = models.DateField(auto_now=False)
    type = models.CharField(max_length=20, default=None)
    cause_profile = models.CharField(max_length=10000, null=True)
    cause_name = models.CharField(max_length=10000, null=True)


class Agency_Social_Media_Post(models.Model):
    author = models.ForeignKey(Agencies, on_delete=models.CASCADE)
    text = models.CharField(max_length=10000, null=True)
    date_posted = models.DateField(auto_now=True)
    link = models.CharField(max_length=200, null=True)
    cause_profile = models.CharField(max_length=10000, null=True)
    cause_name = models.CharField(max_length=10000, null=True)
    agency_profile = models.CharField(max_length=10000, null=True)
    agency_name = models.CharField(max_length=10000, null=True)
    type = models.CharField(max_length=20, default=None)
