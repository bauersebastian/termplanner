import calendar as pycal
from datetime import date, datetime, timedelta, timezone
from io import BytesIO

from allauth.account.forms import LoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
)
from django.views.generic.base import TemplateView
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate

from termplanner.utils.mixins import IsOwnerMixin, IsOwnerOfSemesterModuleMixin

from .forms import EventForm, SemesterModuleForm
from .models import Event, Module, SemesterModule


class SemesterModuleListView(LoginRequiredMixin, ListView):
    model = SemesterModule

    def get_queryset(self):
        return SemesterModule.objects.filter(user=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["semestermodule_list_current"] = (
            SemesterModule.objects.filter(user=self.request.user.id)
            .filter(done=False)
            .annotate(num_events=Count("events"))
            .order_by("-num_events")
        )
        context["semestermodule_list_done"] = SemesterModule.objects.filter(
            user=self.request.user.id
        ).filter(done=True)
        context["ects_done"] = (
            SemesterModule.objects.filter(user=self.request.user.id)
            .filter(done=True)
            .aggregate(Sum("module__ects"))
        )
        user_events = Event.open_objects.select_related("semestermodule").filter(
            semestermodule__user_id=self.request.user.id
        )
        context["events"] = user_events

        return context


class SemesterModuleCreateView(LoginRequiredMixin, CreateView):
    model = SemesterModule
    form_class = SemesterModuleForm

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
    form_class = SemesterModuleForm
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
        context["days_until_exam_a"] = days_until_test(
            semestermodule_id=context["semestermodule"].id,
            event_type=Event.EventType.EXAM_A,
        )
        context["days_until_exam_b"] = days_until_test(
            semestermodule_id=context["semestermodule"].id,
            event_type=Event.EventType.EXAM_B,
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


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = pycal.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = LoginForm()
        return context


def load_modules(request):
    term = request.GET.get("term")
    modules = Module.objects.filter(term=term).order_by("title")
    return render(
        request, "terms/ajax/module_dropdown_list_options.html", {"modules": modules}
    )


def days_until_test(semestermodule_id, event_type):
    day_of_test_event = (
        Event.objects.filter(semestermodule=semestermodule_id)
        .filter(event_type=event_type)
        .first()
    )
    if day_of_test_event:
        testday = day_of_test_event.start_date
        today = datetime.now(timezone.utc)
        delta = testday - today
        if delta.days > 0:
            return delta.days


def events_semestermodule_pdf_view(request):
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )
    sample_style_sheet = getSampleStyleSheet()
    flowables = []
    user_events = Event.open_objects.select_related("semestermodule").filter(
        semestermodule__user_id=request.user.id
    )
    paragraph_1 = Paragraph(
        "Meine laufenden Termine im Semester", sample_style_sheet["Heading1"]
    )
    flowables.append(paragraph_1)
    for event in user_events:
        paragraph_2 = Paragraph(f"{event.title}", sample_style_sheet["BodyText"])
        flowables.append(paragraph_2)
    doc.build(flowables)
    pdf_value = pdf_buffer.getvalue()
    pdf_buffer.close()

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="some_file.pdf"'
    response.write(pdf_value)

    return response
