from django.contrib import admin

from .models import User, Schedule

admin.site.register(User)
admin.site.register(Schedule)