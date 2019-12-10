from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout

from django.core import serializers

from . import forms
from myapp.forms import AgencyForm
from myapp.forms import ProfileForm
from myapp.models import Profile
from . import models




# Helper functions
def checkAuth(request):

  if(request.user.is_authenticated):
      return True
  else:
      return False


# Create your views here.
def home(request):
  title = "Home "
  articles = models.News_Articles.objects.all()[:3]
  Agenciess = models.Agencies.objects.all()
  context = {
    "user" : request.user,
    "title": title,
    "articles": articles,
    "agencies": Agenciess,
    "ranger": range(0, 5),
    "is_user": checkAuth(request),
  }
  return render(request, 'main/index.html', context=context)




def agencies(request):
  title = "Agencies "
  Agenciess = models.Agencies.objects.all()

  context = {
    "title": title,
    "agencies": Agenciess,
    #"cards": newCard,
    "ranger": range(0, 3),
    "is_user": checkAuth(request),
  }
  return render(request, 'main/agencies.html', context=context)




def trending(request):
  title = "Trending News "

  context = {
    "title": title,
    "articles": newArticle,
    "ranger": range(0, 5),
    "is_user": checkAuth(request),
  }
  return render(request, 'main/trending.html', context=context)




def about(request):
  title = "About Us "

  context = {
    "title": title,
    "is_user": checkAuth(request),
  }
  return render(request, 'main/about.html', context = context)




def signIn(request):
  title = "Sign In "

  context = {
    "title": title,
    "is_user": checkAuth(request),
  }

  return render(request, "main/signIn.html", context = context)




def postSignIn(request):
  signedIn = True
  title = "Welcome "
  is_user = request.POST.get('is_user')
  passw = request.POST.get("pass")

  user = authenticate(request, is_user=is_user, password=passw)

  if user is None:
    title = "Invalid "
    message = "invalid credentials"
    signedIn = False

    context = {
      "title": title,
      "msg": message,
      "is_user": checkAuth(request),
    }
    return render(request, "main/signIn.html", context = context)

  context = {
    "title": title,
    "e": is_user,
    "signedIn": signedIn,
    "is_user": checkAuth(request),
  }
  #get.session['uid']=str(session_id)
  return HttpResponseRedirect("main/index.html")




def logout_view(request):
  logout(request)
  return HttpResponseRedirect("/login/")




def signUp(request):
    title = "registration"
    if request.method == "POST":

        form_instance = forms.RegistrationForm(request.POST)
        if form_instance.is_valid():
          form_instance.save()
          return HttpResponseRedirect("/")
    else:
        form_instance = forms.RegistrationForm()

    context = {
        "form":form_instance,
        "title": title,
        "is_user": checkAuth(request),
    }
    return render(request, "registration/signUp.html", context = context)




def postsignup(request):
  title = "Welcome "
  name = request.POST.get('name')
  email = request.POST.get('email')
  passw = request.POST.get('pass')

  context = {
    "title": title,
    "e": email,
    "is_user": checkAuth(request),
  }
  return render(request, "main/welcome.html", context = context)




def agencyProfile(request):
   title = "Agency Profile"
   if checkAuth(request) == False:
       return HttpResponseRedirect("/")
   instance  = get_object_or_404(Profile, user=request.user)
   if instance.agencies is None:
       is_agency = False
   else:
       is_agency = True
   context = {
     "title": title,
     "is_user": checkAuth(request),
     "user": request.user,
     "is_agency": is_agency,
     #Subject to have more things - Calvin
   }
   return render(request, 'main/agencyProfile.html', context=context)




def agencySignUp(request):
  signedIn = True
  is_user = request.POST.get('is_user')
  passw = request.POST.get("pass")

  user = authenticate(request, is_user=is_user, password=passw)


  if request.method == "POST":
    form_instance = forms.AgencyForm(request.POST, request.FILES)
    if form_instance.is_valid():
        instance = form_instance.save(commit=False)
        instance.user = request.user
        instance.save()
        return HttpResponseRedirect("/")

  else:
    form_instance = forms.AgencyForm()

  context = {
    "form" : form_instance,
    "e": is_user,
    "signedIn": signedIn,
    "is_user": checkAuth(request),
  }
  return render(request, 'main/agencySignUp.html', context=context)




def profile(request):
   title = "Profile"
   context = {
     "title": title,
     "is_user": checkAuth(request),
     "user": request.user,
     #Subject to have more things - Calvin
   }
   return render(request, 'main/profile.html', context=context)




def createProfile(request):
  title = "Create Profile"
  signedIn = True
  is_user = request.POST.get('is_user')
  passw = request.POST.get("pass")
  if checkAuth(request) == False:
     return HttpResponseRedirect("/")

  user = authenticate(request, is_user=is_user, password=passw)

  instance  = get_object_or_404(Profile, user=request.user)
  if request.method == "POST":

    form_instance = forms.ProfileForm(request.POST, request.FILES, instance=instance)
    if form_instance.is_valid():
        instance = form_instance.save(commit=False)
        instance.user = request.user
        instance.save()
        return HttpResponseRedirect("/profile/")
  else:
    form_instance = forms.ProfileForm()

    context = {
        "form":form_instance,
        "title": title,
        "is_user": checkAuth(request),
    }
    return render(request, "main/createProfile.html", context = context)
