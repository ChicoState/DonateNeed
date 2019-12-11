from django import forms
from django.core.validators import validate_slug
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from myapp.models import Agencies
from myapp.models import Profile, Cause
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
        exclude = ['user', 'agencies']
        #fields="__all__" #, "picture")


class AddAgencyForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['agencies']


#form to use for updating data in agencies class
class AgencyForm(ModelForm):
   class Meta:
      model = Agencies
      exclude = ['user', 'username', 'causes']

   # causes = forms.ModelMultipleChoiceField(queryset=Cause.objects.all())
   #
   # def __init__(self, *args, **kwargs):
   #      if kwargs.get('instance'):
   #          initial = kwargs.setdefault('initial', {})
   #          initial['causes'] = [t.pk for t in kwargs['instance'].causes_set.all()]
   #      forms.ModelForm.__init__(self, *args, **kwargs)
   #
   #
   # def save(self, commit=True):
   #      instance = forms.ModelForm.save(self, False)
   #      old_save_m2m = self.save_m2m
   #      def save_m2m():
   #         old_save_m2m()
   #         instance.causes_set.clear()
   #         instance.causes_set.add(*self.cleaned_data['causes'])
   #      self.save_m2m = save_m2m
   #
   #      if commit:
   #          instance.save()
   #          self.save_m2m()
   #      return instance


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




class PledgeSupportForm(ModelForm):
    class Meta:
        model = Agencies
        exclude = ['user', 'username', 'name', 'email', 'address', 'url', 'phone', 'username', 'picture']
    # def __init__ (self, *args, **kwargs):
    #     super(PledgeSupportForm, self).__init__(*args, **kwargs)
    #     self.fields["causes"].widget = forms.widgets.CheckboxSelectMultiple()
    #     self.fields["causes"].help_text = ""
    #     self.fields["causes"].queryset = models.Cause.objects.all()
    def clean(self):
        cleaned_data = super().clean()
        causes = cleaned_data.get('causes')



class CauseForm(ModelForm):
    class Meta:
        model= models.Cause
        exclude = ['username']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if title and models.Cause.objects.filter(title=title).count()>1:
            self.add_error('title', forms.ValidationError(('This title already exists. Please be more descriptive'), code='title_error'))
        return cleaned_data
