from django import forms
from django.core.validators import validate_slug
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from myapp.models import Agencies
from myapp.models import Profile, Cause
from django.contrib import messages
import re, string


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


class RegisterDonation(forms.Form):

    class Meta:
        model = models.Request_In_Progress
        fields = ["item", "amount_total", "agency"]
    #
    # def save(self, commit=True):
    #     new_sugg = models.Request_In_Progress(
    #         item=self.cleaned_data["item"],
    #         amount_total=self.cleaned_data["amount_total"]
    #     )
    #     if commit:
    #         new_sugg.save()
    #     return new_sugg
class MakeDonation(ModelForm):
    class Meta:
        model = models.Request_Fulfilled
        exclude = ['user', 'request_in_progress', 'fulfilled_amount']

class MakeDonation(ModelForm):
    class Meta:
        model = models.Request_Fulfilled
        exclude = ['user', 'request_in_progress', 'fulfilled_amount']

class AddRequestForm(ModelForm):
    class Meta:
        model = models.Request_In_Progress
        fields = ["item", "amount_total", "cause", "size"]

class AddVolunteerRequestForm(ModelForm):
    class Meta:
        model = models.Volunteering
        exclude = ["agency", "amount_fulfilled", "percent_complete"]

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'requests_view_hide_completed', 'number_of_donations', 'number_of_volunteering_participations']
        #fields="__all__" #, "picture")


class AddAgencyForm(ModelForm):
    class Meta:
        model = Agencies
        fields = ['admin_users']

# class SelectCityForm(ModelForm):
#     class Meta:
#         model = City
#         fields = ['city_id']

#form to use for updating data in agencies class
class AgencyForm(ModelForm):
   class Meta:
      model = Agencies
      exclude = ['causes']

   def clean(self):
         cleaned_data = super().clean()
         email = cleaned_data.get('email')
         name = cleaned_data.get('name')
         capitalized_name = string.capwords(name)
         uname = (re.sub(r"\s+", "", capitalized_name))
         if Agencies.objects.filter(username=uname).exists():
             print("true")
             self.add_error('name', forms.ValidationError(('This agency name already exists.')))
         if name and Agencies.objects.filter(name=name).count()>1:
             self.add_error('name', forms.ValidationError(('This agency name already exists. If this is your agency, add them to your profile in our profile editor'), code="name_error"))
         if email and Agencies.objects.filter(email=email).exclude(name=name).exists():
             self.add_error('email', forms.ValidationError('This agency email has already been used.', code="email_error"))
         return cleaned_data




class PledgeSupportForm(ModelForm):
    class Meta:
        model = Agencies
        fields = ['causes']
    # def __init__ (self, *args, **kwargs):
    #     super(PledgeSupportForm, self).__init__(*args, **kwargs)
    #     self.fields["causes"].widget = forms.widgets.CheckboxSelectMultiple()
    #     self.fields["causes"].help_text = ""
    #     self.fields["causes"].queryset = models.Cause.objects.all()
    def clean(self):
        cleaned_data = super().clean()
        causes = cleaned_data.get('causes')
        for cause in causes:
            if Agencies.objects.filter(causes=cause).exists():
                self.add_error('causes', forms.ValidationError("One of the causes you selected is already included in your agency's profile"))
                return



class CauseForm(ModelForm):
    class Meta:
        model= Cause
        exclude = ['username']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if title and models.Cause.objects.filter(title=title).count()>1:
            self.add_error('title', forms.ValidationError(('This title already exists. Please be more descriptive'), code='title_error'))
        return cleaned_data


class HideCompletedRequestsForm(ModelForm):
    requests_view_hide_completed = forms.BooleanField(required=False, label='Hide Completed Requests',widget=forms.CheckboxInput(attrs={'onclick': 'this.form.submit()'}))
    class Meta:
        model = Profile
        fields = ['requests_view_hide_completed']
        labels = {
            'requests_view_hide_completed': 'Hide Completed Requests'
        }



class FilterAgencyForm(ModelForm):
    class Meta:
        model = Agencies
        fields = ['name']
