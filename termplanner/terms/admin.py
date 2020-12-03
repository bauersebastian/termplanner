from django.contrib import admin

from .models import Event, Module, SemesterModule

admin.site.register(Module)
admin.site.register(SemesterModule)
admin.site.register(Event)
