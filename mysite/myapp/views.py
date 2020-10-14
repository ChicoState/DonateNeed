from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.db.models import Q
import re, string

from django.core import serializers

from . import forms
from myapp.forms import AgencyForm, ProfileForm, HideCompletedRequestsForm
from myapp.models import Profile, Cause, News_Articles, Agencies, Request_Fulfilled, Request_In_Progress
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
        #
        # delete = request.GET.get('delete', 0)
        #
        # if delete != 0
        #     Request_In_Progress.objects.filter(id=delete).delete()

    title = "Agency Profile"
    if checkAuth(request) == False:
        return HttpResponseRedirect("/")





    try:
        agency = Agencies.objects.get(username=uname)
        requests_in_progress = Request_In_Progress.objects.filter(is_complete=True, agency=agency).count()
        requests_completed = Request_In_Progress.objects.filter(is_complete=False, agency=agency).count()
        if request.user not in agency.admin_users.all():
            is_admin = False
        else:
            is_admin = True

        if request.method == "POST":
            profile = Profile.objects.get(user=request.user)
            print(profile)
            completed_form = HideCompletedRequestsForm(request.POST, instance=profile)
            if(completed_form.is_valid()):
                completed_form.save()
        try:
            profile = Profile.objects.get(user=request.user)
            is_hidden = HideCompletedRequestsForm(instance=profile)
        except:
            is_hidden = HideCompletedRequestsForm()
        hidden_checked = is_hidden['requests_view_hide_completed'].value()
        print(hidden_checked)



        if hidden_checked:
            requests = Request_In_Progress.objects.filter(is_complete=False, agency=agency)
        else:
            requests = Request_In_Progress.objects.filter(agency=agency)

        instance  = models.Profile.objects.get(user=request.user)
        causes = agency.causes

        if  request.user in agency.admin_users.all():
        #if instance.agencies == agency:
            is_personal_agency = True
        else:
            is_personal_agency = False
        is_agency = True
        context = {
            "title": title,
            "is_user": checkAuth(request),
            "user": request.user,
            "username": uname,
            "requests": requests,
            "is_agency":is_agency,
            "is_admin": is_admin,
            "requests_in_progress": requests_in_progress,
            "requests_completed": requests_completed,
            "is_hidden": is_hidden,
            "agency": agency,
             "causes": causes,
            "is_personal_agency": is_personal_agency
        }
        #return HttpResponseRedirect("")
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
            instance = form_instance.save(commit = False)
            instance.user = request.user

            name = string.capwords(instance.name)
            uname = re.sub(r"\s+", "", name)
            instance.username = uname
            instance.save()
            instance.admin_users.add(request.user)
            return redirect("main/agencySignUp.html")
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
    user_agency = []
    try:
        user_info = models.User.objects.get(username=username)
        if user_info == request.user:
            is_personal_profile = True
            user = request.user
            profile = Profile.objects.get(user=request.user)
            all_agencies = Agencies.objects.all()
            for agency in all_agencies:
                if request.user in agency.admin_users.all():
                    has_agency = True
                    user_agency.append(agency)

            #for agency in all_agencies
            #if Agencies.objects.filter(user__in=admin_users) is not None:

            #if Agencies.admin_users.filter(user__in=admin_users) is not None:
            #if request.user.profile.agencies is not None:
                #has_agency = True
        else:
           is_personal_profile = False

        is_an_account = True
        context = {
            "title": title,
            "is_user": checkAuth(request),
            "user": request.user,
            "username": username,
            "user_agency": user_agency,
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
            print(instance.username)
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



def pledgeSupport(request,  username=None):
    agency = Agencies.objects.get(username=username)
    if checkAuth(request) == False:
        return HttpResponseRedirect("/")

    if request.user not in agency.admin_users.all():
        return HttpResponseRedirect("/")


    if request.method == "POST":
        form_instance = forms.PledgeSupportForm(request.POST, instance=agency)
        if form_instance.is_valid():
            ids = request.POST.get('causes')
            for id in ids:
                agency.causes.add(id)
            causes = agency.causes.all()
            context = {
                "username": username,
                "is_agency": True,
                "user": request.user,
                "agency": agency,
                "causes": causes,
                "is_personal_agency": True
            }
            return render(request, 'main/agencyProfile.html', context=context)
    else:
        form_instance = forms.PledgeSupportForm()
    context = {
        "form" : form_instance,
        "username": username,
        "is_user": checkAuth(request),
    }
    return render(request, 'main/pledgeSupport.html', context=context)



@csrf_exempt
def donation(request, username):
  agency1 = Agencies.objects.filter(username=username)
  agency = agency1[0]
  form_instance = forms.RegisterDonation()
  if form_instance.is_valid():
      instance = form_instance.save(commit=False)
      instance.agency = agency
      instance.save()


  context = {
      "title":"Suggestion Form",
      "form":form_instance,
      "agency": agency
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
            new_donation.agency = request.user.profile.agencies

            new_donation.save()

        for sub in updates:
            next_item = models.Request_In_Progress.objects.get(id=sub['id'])
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


def addAgency(request, username=None):
    agency = Agencies.objects.get(username=username)
    if checkAuth(request) == False:
        return HttpResponseRedirect("/")

    if request.method == "POST":
        form_instance = forms.AddAgencyForm(request.POST, instance=agency)
        if form_instance.is_valid():
            f_instance = form_instance.save(commit=False)
            users = form_instance.cleaned_data['admin_users']
            for user in users:
                agency.admin_users.add(user)
            agency.save()
            return redirect('/')
    else:
        form_instance = forms.AddAgencyForm()
    context = {
        "form" : form_instance,
        "instance": agency,
        "username": username,
        "is_user": checkAuth(request),
    }
    #return redirect(addAgency, username=username)
    return render(request, 'main/addAgency.html', context=context)




def activeCauses(request):
    cause = Cause.objects.all()
    context = {
        "Cause": cause,
        "is_user": checkAuth(request)
    }
    return render(request, 'main/activeCauses.html', context=context)




def causePage(request, uname=None):
    title = "Cause"
    username = re.sub(r"\s+", "", uname)
    if checkAuth(request) == False:
        return HttpResponseRedirect("/")
    try:
        cause_info = Cause.objects.get(username=username)
        requests = Request_In_Progress.objects.filter(cause=cause_info.id)
        article1 = News_Articles.objects.filter(description__contains=uname)
        article2  = News_Articles.objects.filter(title__contains=uname)
        agencies = Agencies.objects.filter(causes=cause_info)
        #if request.user not in agency.admin_users.all():
        if request.method == 'POST':
            agency_id = request.POST.get('agency_id')
            if agency_id is not "":
                selected_item = get_object_or_404(Agencies, pk=request.POST.get('agency_id'))
                requests = Request_In_Progress.objects.filter(agency=selected_item, cause=cause_info.id)

        articles = article1 | article2
        is_cause = True
        context = {
            "title": title,
            "is_user": checkAuth(request),
            "user": request.user,
            "uname": uname,
            "agencies": agencies,
            "is_cause": is_cause,
            "articles": articles,
            "requests": requests,
            "cause_info": cause_info,
        }
        return render(request, 'main/cause.html', context=context )

    except models.Cause.DoesNotExist:
        return redirect('activeCauses')



def agencyRequestedDonations(request, username=None):
    if checkAuth(request) == False:
        return HttpResponseRedirect("/")
    if(username is None):
        requests = Request_In_Progress.objects.all()
        is_admin = False
        agency = "All Agency"
    else:
        agency = Agencies.objects.filter(username=username)[0]
        if request.user in agency.admin_users.all():
            is_admin = True
        else:
            is_admin = False
        requests = Request_In_Progress.objects.filter(agency=agency)

    delete = request.GET.get('delete', 0)
    context = {
        "agency": agency,
        "username": username,
        "user": request.user,
        "is_admin": is_admin,
        "is_user": checkAuth(request),
        "requests": requests,
    }
    if delete != 0:
        Request_In_Progress.objects.filter(id=delete).delete()

    return render(request, 'main/agencyRequestedDonations.html', context=context)



def addRequests(request, username):
    if checkAuth(request) == False:
        return HttpResponseRedirect("/")
    agency = Agencies.objects.filter(username=username)[0]
    if request.user not in agency.admin_users.all():
        return HttpResponseRedirect("/")
    if request.method == "POST":
        form_instance = forms.AddRequestForm(request.POST)
        if form_instance.is_valid():
          instance = form_instance.save(commit=False)
          cause = form_instance.cleaned_data['cause']
          if cause not in agency.causes.all():
              agency.causes.add(cause)
          instance.agency = agency
          instance.save()
          return redirect('activeDonations')
    else:
        form_instance = forms.AddRequestForm()

    context = {
      "form":form_instance,
      "username": username,
      "agency": agency,
      "is_user": checkAuth(request),
    }
    return render(request, 'main/addRequests.html', context=context)



def activeDonations(request):
    if checkAuth(request) == False:
        return HttpResponseRedirect("/")

    agencies = Agencies.objects.all()
    causes = Cause.objects.all()
    requests = Request_In_Progress.objects.all()
    if request.method == 'POST':
        agency_id = request.POST.get('agency_id')
        if agency_id is not "":
            selected_item = get_object_or_404(Agencies, pk=request.POST.get('agency_id'))
            requests = Request_In_Progress.objects.filter(agency=selected_item)
        cause_id = request.POST.get('cause_id')
        if cause_id is not "":
            selected_cause = get_object_or_404(Agencies, pk=request.POST.get('cause_id'))
            requests = Request_In_Progress.objects.filter(agency=selected_cause)

    user = request.user
    context = {
        "user": user,
        "agencies": agencies,
        "causes": causes,
        "is_user": checkAuth(request),
        "requests": requests
    }

    return render(request, 'main/activeDonations.html', context = context)




def finalSubmitDonation(request, id):

    if checkAuth(request) == False:
        return HttpResponseRedirect("/")
    donation = Request_In_Progress.objects.filter(id=id)[0]

    if request.method == "POST":
        form_instance = forms.MakeDonation(request.POST)
        if form_instance.is_valid():

          instance = form_instance.save(commit=False)
          instance.user = request.user
          instance.request_in_progress = donation
          instance.fulfilled_amount = 0
          instance.save()

          pledged = form_instance.cleaned_data['promised_amount']
          fulfilled = donation.amount_fulfilled
          total = donation.amount_total

          donation.amount_fulfilled = pledged+fulfilled
          donation.percent_complete = ((pledged+fulfilled)/total)*100

          if(donation.amount_fulfilled == donation.amount_total):
              donation.is_complete = True
              donation.percent_complete = 100
          donation.save()
          return redirect('submitDonations')
    else:
        form_instance = forms.MakeDonation()

    user = request.user
    context = {
        "user": user,
        "id": id,
        "is_user": checkAuth(request),
        "form": form_instance,
        "donation": donation
    }

    return render(request, 'main/finalSubmitDonation.html', context = context)


def search(request):
    if request.method == 'GET' and 'q' in request.GET:
        keyword = request.GET['q']
    else:
        keyword is None

    if keyword is not None and keyword != '':
        agencies = Agencies.objects.filter(Q(name__contains=keyword) | Q(username__contains=keyword))
        causes = Cause.objects.filter(Q(title__contains=keyword) | Q(location__contains=keyword))
        users = User.objects.filter(Q(first_name__contains = keyword) | Q(last_name__contains = keyword) | Q(username__contains = keyword))
        news_articles = News_Articles.objects.filter(Q(title__contains = keyword) | Q(description__contains = keyword))

    else:
        print("made it")
        agencies = None
        causes = None
        users = None
        news_articles = None

    context = {
        "agencies": agencies,
        "news_articles": news_articles,
        "users": users,
        "is_user": checkAuth(request),
        "causes": causes,
    }
    return render(request, 'main/search.html', context=context)
