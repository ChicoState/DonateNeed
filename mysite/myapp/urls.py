from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
  url(r'^$', views.home, name='home'),
  url(r'^agencies$', views.agencies, name='agencies'),
  url(r'^trending$', views.trending, name='trending'),
  url(r'^about$', views.about, name='about'),
  url(r'^signIn$', path('login/', auth_views.LoginView.as_view()),),
  url(r'^postSignIn/', views.postSignIn, name='postsign'),
  url(r'^logout$', views.logout, name='logout'),
  url(r'^signUp$', views.signUp, name='signUp'),
  url(r'^postsignup/', views.postsignup, name='postsignup')
]
