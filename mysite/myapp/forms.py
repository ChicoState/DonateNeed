from django import forms
from django.core.validators import validate_slug
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from myapp.models import Agencies


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
                  "password1", "password2")

    def save(self, commit=True):

        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:

            user.save()
        return user


#form to use for updating data in agencies class
class AgencyForm(ModelForm):
  class Meta:
     model = Agencies
     fields = '__all__'
