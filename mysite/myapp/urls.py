from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
  url(r'^$', views.home, name='home'),
  url(r'^agencies$', views.agencies, name='agencies'),
  url(r'^trending$', views.trending, name='trending'),
  url(r'^about$', views.about, name='about'),
  url('login/', auth_views.LoginView.as_view(), name='login'),
  url(r'^postSignIn/', views.postSignIn, name='postsignin'),
  url('logout/', views.logout_view, name='logout'),
  url(r'^signUp$', views.signUp, name='signUp'),
  url(r'^donation/', views.donation, name='donation'),
  url(r'^fetch_donation/', views.fetch_donation, name='fetch_donation'),
  url(r'^agencySignUp/', views.agencySignUp, name='agencySignUp'),
  url(r'^profile/(?P<username>.+)/', views.profile, name='profile'),
  url(r'^createProfile/', views.createProfile, name='createProfile'),
  url(r'^agencyProfile/(?P<uname>.+)', views.agencyProfile, name='agencyProfile'),
  url(r'^createCause/', views.createCause, name='createCause'),
  url(r'^addAgency/', views.addAgency, name='addAgency'),
  url(r'^pledgeSupport/', views.pledgeSupport, name='pledgeSupport'),
  url(r'^cause/(?P<username>.+)', views.causePage, name='causePage'),
]
