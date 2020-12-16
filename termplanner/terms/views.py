from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
)

from termplanner.utils.mixins import IsOwnerMixin, IsOwnerOfSemesterModuleMixin

from .forms import EventForm
from .models import Event, SemesterModule


class SemesterModuleListView(LoginRequiredMixin, ListView):
    model = SemesterModule

    def get_queryset(self):
        return SemesterModule.objects.filter(user=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["semestermodule_list_current"] = SemesterModule.objects.filter(
            user=self.request.user.id
        ).filter(done=False)
        context["semestermodule_list_done"] = SemesterModule.objects.filter(
            user=self.request.user.id
        ).filter(done=True)
        return context


class SemesterModuleCreateView(LoginRequiredMixin, CreateView):
    model = SemesterModule
    fields = ["module", "term", "points_sl", "points_exam", "grade"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EventCreateView(LoginRequiredMixin, FormView):
    form_class = EventForm
    template_name = "terms/event_form.html"

    def get_success_url(self):
        semestermodule_id = self.kwargs["semestermodule_id"]
        return reverse_lazy("terms:detail", kwargs={"pk": semestermodule_id})

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
    fields = ["module", "term", "points_sl", "points_exam", "grade", "done"]
    action = "Update"


class EventUpdateView(LoginRequiredMixin, IsOwnerOfSemesterModuleMixin, UpdateView):
    model = Event
    fields = ["title", "note", "start_date", "end_date", "done", "event_type"]
    action = "Update"


class SemesterModuleDetailView(LoginRequiredMixin, IsOwnerMixin, DetailView):
    model = SemesterModule

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event_list"] = Event.objects.filter(
            semestermodule=context["semestermodule"].id
        )
        return context


class EventDetailView(LoginRequiredMixin, IsOwnerOfSemesterModuleMixin, DetailView):
    model = Event


class SemesterModuleDeleteView(LoginRequiredMixin, IsOwnerMixin, DeleteView):
    model = SemesterModule
    success_url = reverse_lazy("terms:list")


class EventDeleteView(LoginRequiredMixin, IsOwnerOfSemesterModuleMixin, DeleteView):
    model = Event

    def get_success_url(self):
        semestermodule_id = self.kwargs["semestermodule_id"]
        return reverse_lazy("terms:detail", kwargs={"pk": semestermodule_id})
