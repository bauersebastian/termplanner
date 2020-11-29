from django.urls import path

from . import views

app_name = "terms"
urlpatterns = [
    path(route="", view=views.SemesterModuleListView.as_view(), name="list"),
    path(route="add/", view=views.SemesterModuleCreateView.as_view(), name="add"),
    path(
        route="<int:pk>/update/",
        view=views.SemesterModuleUpdateView.as_view(),
        name="update",
    ),
    path(
        route="<int:pk>/", view=views.SemesterModuleDetailView.as_view(), name="detail"
    ),
]
