from django.contrib import admin

from .models import Module, SemesterModule

admin.site.register(Module)
admin.site.register(SemesterModule)
