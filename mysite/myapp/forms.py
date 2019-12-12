from django import forms
from django.core.validators import validate_slug
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

class RegisterDonation(forms.Form):
    
    class Meta:
        model = models.Request_In_Progress
        fields = ["item", "amount_total"]

    def save(self, commit=True):
        new_sugg = models.Request_In_Progress(
            item=self.cleaned_data["item"],
            amount_total=self.cleaned_data["amount_total"]
        )
        if commit:
            new_sugg.save()
        return new_sugg