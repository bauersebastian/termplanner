from django.urls import path

from . import views

app_name = "terms"
urlpatterns = [
    # Semestermodule paths
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
    # Events paths
    path(
        route="<int:semestermodule_id>/event/<int:pk>",
        view=views.EventDetailView.as_view(),
        name="detail_event",
    ),
    path(
        route="event/<int:pk>/update/",
        view=views.EventUpdateView.as_view(),
        name="update_event",
    ),
    path(
        route="<int:semestermodule_id>/event/add/",
        view=views.EventCreateView.as_view(),
        name="add_event",
    ),
]
