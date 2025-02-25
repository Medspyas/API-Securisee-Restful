from django.contrib import admin

from .models import Contributor, Project

admin.site.register(Project)
admin.site.register(Contributor)
