from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView  # TODO: UpdateView, CreateView, DetailView

from .models import SemesterModule

# from termplanner.utils.mixins import IsOwnerMixin


class SemesterModuleListView(LoginRequiredMixin, ListView):
    model = SemesterModule

    def get_queryset(self):
        return SemesterModule.objects.filter(user=self.request.user.id)
