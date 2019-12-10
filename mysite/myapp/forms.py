from django import forms
from django.core.validators import validate_slug
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from myapp.models import Agencies
from myapp.models import Profile
from django.contrib import messages



from . import models


# Add your forms
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True
        )

    class Meta:
        model = User
        fields = ("username", "email",
                  "password1", "password2",
                  "first_name", "last_name")
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            self.add_error('email', 'This email address is already associated with an account. Please use a different email.')
        return cleaned_data


    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:

            user.save()
        return user


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        #fields="__all__" #, "picture")

#form to use for updating data in agencies class
class AgencyForm(ModelForm):
  class Meta:
   model = Agencies
   exclude = ['user']

  def clean(self):
     cleaned_data = super().clean()
     email = cleaned_data.get('email')
     name = cleaned_data.get('name')
     if name and Agencies.objects.filter(name=name).count()>1:
         if not self.has_error('name', "name_error"):
             self.add_error('name', forms.ValidationError(('This agency name already exists. If this is your agency, add them to your profile in our profile editor'), code="name_error"))
     if email and Agencies.objects.filter(email=email).exclude(name=name).exists():
         if not self.has_error('email', "email_error"):
             self.add_error('email', forms.ValidationError('This agency email has already been used.', code="email_error"))
     return cleaned_data
