from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
import re

from django.core import serializers

from . import forms
from myapp.forms import AgencyForm
from myapp.forms import ProfileForm
from myapp.models import Profile
from . import models

import json



# Helper functions
def checkAuth(request):
    if(request.user.is_authenticated):
        return True
    else:
        return False


# Create your views here.
def home(request):
    title = "Home "
    articles = models.News_Articles.objects.all().order_by('-picture')
    articles = articles[:4]
    Agenciess = models.Agencies.objects.all()[:6]
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
        "ranger": range(0, 3),
        "is_user": checkAuth(request),
    }
    return render(request, 'main/agencies.html', context=context)




def trending(request):
    title = "Trending News "
    articles = models.News_Articles.objects.all().order_by('-picture')
    # articles = articles[:10]

    context = {
        "title": title,
        "articles": articles,
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
            user = request.user
            context = {
                "user":user,
                "is_user": checkAuth(request),
            }
            # return render(request, "main/signIn.html", context = context)
            return HttpResponseRedirect("/")

    else:
        form_instance = forms.RegistrationForm()

    context = {
        "form":form_instance,
        "title": title,
        "is_user": checkAuth(request),
    }
    return render(request, "registration/signUp.html", context = context)




# def postsignup(request):
#     title = "Welcome "
#     name = request.POST.get('name')
#   email = request.POST.get('email')
#   passw = request.POST.get('pass')
#
#   context = {
#     "title": title,
#     "e": email,
#     "is_user": checkAuth(request),
#   }
#   return render(request, "main/welcome.html", context = context)




def agencyProfile(request, uname=None):
    title = "Agency Profile"
    print(uname)
    if checkAuth(request) == False:
        return HttpResponseRedirect("/")

    try:
        agency = models.Agencies.objects.get(username=uname)
        instance  = models.Profile.objects.get(user=request.user)
        causes = agency.causes

        if instance.agencies == agency:
            is_personal_agency = True
        else:
            is_personal_agency = False
        is_agency = True
        context = {
            "title": title,
            "is_user": checkAuth(request),
            "user": request.user,
            "username": uname,
            "is_agency":is_agency,
            "agency": agency,
             "causes": causes,
            "is_personal_agency": is_personal_agency
        }
        return render(request, 'main/agencyProfile.html', context=context)

    except models.Agencies.DoesNotExist:
        is_agency = False
        is_personal_agency = False
    context = {
        "title": title,
        "is_user": checkAuth(request),
        "user": request.user,
        "is_agency": is_agency,
        "is_personal_agency": is_personal_agency,
        "username": uname,
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
            name = instance.name
            instance.username = re.sub(r"\s+", "", name)
            instance.save()
            return redirect("/")
    else:
        form_instance = forms.AgencyForm()
    context = {
        "form" : form_instance,
        "e": is_user,
        "signedIn": signedIn,
        "is_user": checkAuth(request),
    }
    return render(request, 'main/agencySignUp.html', context=context)




def profile(request, username=None):
    title = "Profile"
    if checkAuth(request) == False:
        return HttpResponseRedirect("/")
    has_agency = False
    try:
        user_info = models.User.objects.get(username=username)
        if user_info == request.user:
            is_personal_profile = True
            if request.user.profile.agencies is not None:
                has_agency = True
        else:
           is_personal_profile = False

        is_an_account = True
        context = {
            "title": title,
            "is_user": checkAuth(request),
            "user": request.user,
            "username": username,
            "is_an_account":is_an_account,
            "user_info": user_info,
            "has_agency": has_agency,
            "is_personal_profile": is_personal_profile,
        }
        return render(request, 'main/profile.html', context=context)
    except models.User.DoesNotExist:
        return HttpResponseRedirect("/")
    #     is_an_account = False
    # is_personal_profile = False
    # context = {
    #     "title": title,
    #     "is_user": checkAuth(request),
    #     "user": request.user,
    #     "username": username,
    #     "is_an_account":is_an_account,
    #     "is_personal_profile": is_personal_profile,
    #     "has_agency": has_agency,
    # }
    # return render(request, 'main/profile.html', context=context)



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
            username = instance.user.username
            instance.save()
            return redirect('profile', username=username)
    else:
        form_instance = forms.ProfileForm()
    context = {
        "form":form_instance,
        "title": title,
        "is_user": checkAuth(request),
    }
    return render(request, "main/createProfile.html", context = context)



def createCause(request):
    title = "Create Cause"
    signedIn = True
    is_user = request.POST.get('is_user')
    passw = request.POST.get("pass")
    if checkAuth(request) == False:
        return HttpResponseRedirect("/")

    if request.method == "POST":
        form_instance = forms.CauseForm(request.POST)
        if form_instance.is_valid():
            instance = form_instance.save(commit=False)
            title = instance.title
            instance.username = re.sub(r"\s+", "", title)
            instance.save()
            return HttpResponseRedirect("/")
    else:
        form_instance = forms.CauseForm()
    context = {
        "form" : form_instance,
        "e": is_user,
        "signedIn": signedIn,
        "is_user": checkAuth(request),
    }
    return render(request, 'main/createCause.html', context=context)




def pledgeSupport(request):
    title = "Pledge Support to a Cause"
    signedIn = True
    is_user = request.POST.get('is_user')
    passw = request.POST.get("pass")
    if checkAuth(request) == False:
        return HttpResponseRedirect("/")

    instance  = models.Profile.objects.get(user=request.user)
    if instance.agencies is None:
        return HttpResponseRedirect("/")
    agency_name = instance.agencies.name
    agency = instance
    if agency is None:
        is_agency = False
    else:
        is_agency = True

    if request.method == "POST":
        form_instance = forms.PledgeSupportForm(request.POST)
        if form_instance.is_valid():
            id = request.POST.get('causes')
            agency = models.Agencies.objects.get(name = agency_name)
            agency.causes.add(id)
            return HttpResponseRedirect("/")
    else:
        form_instance = forms.PledgeSupportForm()
    context = {
        "form" : form_instance,
        "e": is_user,
        "signedIn": signedIn,
        "is_agency": is_agency,
        "is_user": checkAuth(request),
    }
    return render(request, 'main/pledgeSupport.html', context=context)



@csrf_exempt
def donation(request):

  form_instance = forms.RegisterDonation()
  context = {
      "title":"Suggestion Form",
      "form":form_instance
  }
  return render(request, "main/donation.html", context=context)


@csrf_exempt
def fetch_donation(request):

    if request.method == "POST":

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        additions = body['add_donations']
        updates = body['donations']
        
        for sub in additions:
            
            new_donation = models.Request_In_Progress()
            new_donation.item = sub['item']
            new_donation.amount_total = sub['amount']

            new_donation.save()

        for sub in updates:
            print("old value")
            next_item = models.Request_In_Progress.objects.get(id=sub['id'])
            print(next_item.item)
            next_item.item = sub['item']
            next_item.amount_total = sub['amount']
            next_item.save()

    donations = models.Request_In_Progress.objects.all()
    donation_list = {"donations":[]}

    for donation in donations:
        donation_list["donations"] += [{
        "item":donation.item,
        "amount":donation.amount_total,
        "id":donation.id
        }]

    print(donation_list)

    return JsonResponse(donation_list)


def addAgency(request):
    title = "Pledge Support to a Cause"
    signedIn = True
    is_user = request.POST.get('is_user')
    passw = request.POST.get("pass")
    if checkAuth(request) == False:
        return HttpResponseRedirect("/")

    instance  = models.Profile.objects.get(user=request.user)


    if request.method == "POST":
        form_instance = forms.AddAgencyForm(request.POST, instance=instance)
        if form_instance.is_valid():
            instance = form_instance.save(commit=False)
            instance.user = request.user
            username = instance.user.username
            instance.save()
            return redirect('profile', username=username)
    else:
        form_instance = forms.AddAgencyForm()
    context = {
        "form" : form_instance,
        "e": is_user,
        "signedIn": signedIn,
        "instance": instance,
        "is_user": checkAuth(request),
    }
    return render(request, 'main/addAgency.html', context=context)



def causePage(request, username=None):
    title = "Cause"
    if checkAuth(request) == False:
        return HttpResponseRedirect("/")
    cause_info = username
    try:
        cause_info = models.Cause.objects.get(username=username)
        is_cause = True

    except models.Cause.DoesNotExist:
        is_cause = False
    context = {
        "title": title,
        "is_user": checkAuth(request),
        "user": request.user,
        "username": username,
        "is_cause": is_cause,
        "cause_info": cause_info,
    }
    return render(request, 'main/cause.html', context=context)
