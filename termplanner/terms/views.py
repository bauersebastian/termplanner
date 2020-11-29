from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from termplanner.utils.mixins import IsOwnerMixin

from .models import SemesterModule


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


class SemesterModuleUpdateView(LoginRequiredMixin, IsOwnerMixin, UpdateView):
    model = SemesterModule
    fields = ["module", "term", "points_sl", "points_exam", "grade"]
    action = "Update"


class SemesterModuleDetailView(LoginRequiredMixin, IsOwnerMixin, DetailView):
    model = SemesterModule
