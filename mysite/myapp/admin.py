from django.contrib import admin
from .models import Profile, Agencies, News_Articles, Cause


admin.site.register(Profile)
admin.site.register(Cause)
admin.site.register(Agencies)
admin.site.register(News_Articles)
