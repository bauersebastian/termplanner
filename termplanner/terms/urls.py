from django.urls import path

from . import views

app_name = "terms"
urlpatterns = [path(route="", view=views.SemesterModuleListView.as_view(), name="list")]
