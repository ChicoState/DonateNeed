from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
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
  url(r'^postsignup$', views.postsignup, name='postsignup'),
  url(r'^agencySignUp/', views.agencySignUp, name='agencySignUp'),
  url(r'^profile/', views.profile, name='profile')
]
