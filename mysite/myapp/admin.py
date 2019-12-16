from django.contrib import admin
from . import models


admin.site.register(models.Profile)
admin.site.register(models.Cause)
admin.site.register(models.Agencies)
admin.site.register(models.News_Articles)
admin.site.register(models.Request_In_Progress)
