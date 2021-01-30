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
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from termplanner.utils.mixins import IsOwnerMixin, IsOwnerOfSemesterModuleMixin

from .forms import EventForm, SemesterModuleForm
from .models import Event, Module, SemesterModule


class SemesterModuleListView(LoginRequiredMixin, ListView):
    model = SemesterModule

    def calculate_competences(self):
        done_modules = SemesterModule.objects.filter(user=self.request.user.id).filter(
            done=True
        )
        count_modules = done_modules.count()
        if count_modules is None or count_modules == 0:
            return None
        wiwi = 0
        cs = 0
        key = 0
        infosys = 0
        for enrollment in done_modules:
            if enrollment.module.quota_economics:
                wiwi += enrollment.module.quota_economics
            if enrollment.module.quota_cs:
                cs += enrollment.module.quota_cs
            if enrollment.module.quota_is:
                infosys += enrollment.module.quota_is
            if enrollment.module.quota_key_competence:
                key += enrollment.module.quota_key_competence
        wiwi_percent = wiwi / count_modules
        cs_percent = cs / count_modules
        key_percent = key / count_modules
        infosys_percent = infosys / count_modules
        competences = dict()
        competences["wiwi"] = wiwi_percent
        competences["cs"] = cs_percent
        competences["key"] = key_percent
        competences["infosys"] = infosys_percent
        return competences

    def get_queryset(self):
        return SemesterModule.objects.filter(user=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["semestermodule_list_current"] = (
            SemesterModule.objects.filter(user=self.request.user.id)
            .filter(done=False)
            .annotate(num_events=Count("events"))
            .order_by("term", "-num_events")
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
        context["competences"] = self.calculate_competences()

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
    semestermodules = (
        SemesterModule.objects.filter(user=request.user.id)
        .filter(done=False)
        .annotate(num_events=Count("events"))
        .order_by("-num_events")
    )
    headline = Paragraph("Termine im Semester", sample_style_sheet["Heading1"])
    flowables.append(headline)
    for module in semestermodules:
        event_query = module.events.filter(done=False)

        module_headline = Paragraph(module.module.title, sample_style_sheet["Heading2"])
        flowables.append(module_headline)
        if not event_query:
            no_events = Paragraph(
                "Keine offenen Termine im Modul", sample_style_sheet["BodyText"]
            )
            flowables.append(no_events)
        data = []
        for event in event_query:
            line = []
            if event.all_day:
                formatted_start_date = event.start_date.astimezone().strftime(
                    "%d.%m.%Y"
                )
                formatted_end_date = event.end_date.astimezone().strftime("%d.%m.%Y")
                line.append(
                    Paragraph(
                        f"{formatted_start_date} bis {formatted_end_date}",
                        sample_style_sheet["BodyText"],
                    )
                )
            else:
                if event.end_date:
                    formatted_start_date = event.start_date.astimezone().strftime(
                        "%d.%m.%Y - %H:%M"
                    )
                    formatted_end_date = event.end_date.astimezone().strftime(
                        "%H:%M Uhr"
                    )
                    line.append(
                        Paragraph(
                            f"{formatted_start_date} bis {formatted_end_date}",
                            sample_style_sheet["BodyText"],
                        )
                    )
                else:
                    formatted_start_date = event.start_date.astimezone().strftime(
                        "%d.%m.%Y - %H:%M Uhr"
                    )
                    line.append(f"{formatted_start_date}")
            line.append(Paragraph(f"{event.title}", sample_style_sheet["BodyText"]))
            line.append(
                Paragraph(
                    f"{event.get_event_type_display()}", sample_style_sheet["BodyText"]
                )
            )

            if line:
                data.append(line)
                if event.note:
                    second_line = []
                    note = [Paragraph(f"{event.note}", sample_style_sheet["BodyText"])]
                    second_line.append("Notiz:")
                    second_line.append(note)
                    data.append(second_line)
                else:
                    data.append([])
        if data:
            tstyle = []
            for i, row in enumerate(data):
                if i % 2 == 0:
                    tstyle.append(("LINEABOVE", (0, i), (-1, i), 1, colors.grey))
                    tstyle.append(("SPAN", (1, i + 1), (2, i + 1)))
            t = Table(data, colWidths=(6 * cm, 6 * cm, 4 * cm))
            t.setStyle(TableStyle(tstyle))
            flowables.append(t)
            flowables.append(Spacer(1 * cm, 5 * mm))

    doc.build(flowables)
    pdf_value = pdf_buffer.getvalue()
    pdf_buffer.close()

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="vawi_termine.pdf"'
    response.write(pdf_value)

    return response
