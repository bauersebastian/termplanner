from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, FormView, ListView, UpdateView

from termplanner.utils.mixins import IsOwnerMixin, IsOwnerOfSemesterModuleMixin

from .forms import EventForm
from .models import Event, SemesterModule


class SemesterModuleListView(LoginRequiredMixin, ListView):
    model = SemesterModule

    def get_queryset(self):
        return SemesterModule.objects.filter(user=self.request.user.id)


class SemesterModuleCreateView(LoginRequiredMixin, CreateView):
    model = SemesterModule
    fields = ["module", "term", "points_sl", "points_exam", "grade"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EventCreateView(LoginRequiredMixin, FormView):
    form_class = EventForm
    template_name = "terms/event_form.html"
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        """
        Overridden so we can make sure the `SemesterModule` instance exists
        before going any further.
        """
        self.semestermodule = get_object_or_404(
            SemesterModule, pk=kwargs["semestermodule_id"]
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.semestermodule = self.semestermodule
        form.instance.save()
        return super().form_valid(form)


class SemesterModuleUpdateView(LoginRequiredMixin, IsOwnerMixin, UpdateView):
    model = SemesterModule
    fields = ["module", "term", "points_sl", "points_exam", "grade"]
    action = "Update"


class EventUpdateView(LoginRequiredMixin, IsOwnerOfSemesterModuleMixin, UpdateView):
    model = Event
    fields = ["title", "note", "start_date", "end_date", "done", "event_type"]
    action = "Update"


class SemesterModuleDetailView(LoginRequiredMixin, IsOwnerMixin, DetailView):
    model = SemesterModule


class EventDetailView(LoginRequiredMixin, IsOwnerOfSemesterModuleMixin, DetailView):
    model = Event
