from django.conf.urls import url
from dal import autocomplete
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .models import Cause

urlpatterns = [
  url(r'^$', views.home, name='home'),
  url(r'^agencies$', views.agencies, name='agencies'),
  url(r'^volunteering$', views.volunteering, name='volunteering'),
  url(r'^trending$', views.trending, name='trending'),
  url(r'^about$', views.about, name='about'),
  url('login/', auth_views.LoginView.as_view(), name='login'),
  url(r'^postSignIn/', views.postSignIn, name='postsignin'),
  url('logout/', views.logout_view, name='logout'),
  url(r'^signUp$', views.signUp, name='signUp'),
  url(r'^agencySignUp/', views.agencySignUp, name='agencySignUp'),
  url(r'^profile/(?P<username>.+)/', views.profile, name='profile'),
  url(r'^agencyRequestedDonations/(?P<username>.+)/', views.agencyRequestedDonations, name='agencyRequestedDonations'),
  url(r'^agencyRequestedDonations/', views.agencyRequestedDonations, name='agencyRequestedDonations'),
  url(r'^agencyRequestedVolunteers/(?P<username>.+)/', views.agencyRequestedVolunteers, name='agencyRequestedVolunteers'),
  url(r'^agencyRequestedVolunteers/', views.agencyRequestedVolunteers, name='agencyRequestedVolunteers'),
  url(r'^addRequests/(?P<username>.+)/', views.addRequests, name='addRequests'),
  url(r'^addVolunteerRequest/(?P<username>.+)/', views.addVolunteerRequest, name='addVolunteerRequest'),
  url(r'^createProfile/', views.createProfile, name='createProfile'),
  url(r'^agencyProfile/(?P<uname>.+)', views.agencyProfile, name='agencyProfile'),
  url(r'^createCause/', views.createCause, name='createCause'),
  url(r'^addAgency/(?P<username>.+)', views.addAgency, name='addAgency'),
  url(r'^pledgeSupport/(?P<username>.+)/', views.pledgeSupport, name='pledgeSupport'),
  url(r'^activeCauses/', views.activeCauses, name='activeCauses'),
  url(r'^cause/(?P<uname>.+)', views.causePage, name='causePage'),
  url(r'^activeDonations/', views.activeDonations, name='activeDonations'),
  url(r'^activeVolunteerRequests/', views.activeVolunteerRequests, name='activeVolunteerRequests'),
  url(r'^search/', views.search, name='search'),
  path('serve_shiny/', include('serve_shiny.urls')),
  url(r'^finalSubmitDonation/(?P<id>.+)/', views.finalSubmitDonation, name='finalSubmitDonation'),
  url(r'^PledgeToVolunteer/(?P<id>.+)/', views.PledgeToVolunteer, name='PledgeToVolunteer'),
  url('test-autocomplete/$', autocomplete.Select2QuerySetView.as_view(model=Cause), name='select2_fk',),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
