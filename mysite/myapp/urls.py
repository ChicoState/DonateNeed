from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
  url(r'^admin/', admin.site.urls),
  url(r'^$', views.home, name='home'),
  url(r'^agencies$', views.agencies, name='agencies'),
  url(r'^trending$', views.trending, name='trending'),
  url(r'^about$', views.about, name='about'),
  url(r'^signIn$', views.signIn, name='signIn'),
  url(r'^postsign$', views.postsign, name='postsign')
]
