import datetime

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel


class Module(TimeStampedModel):
    title = models.CharField("Titel des Moduls", max_length=255)
    short_title = models.CharField("Abkürzung des Moduls", max_length=5)
    description = models.TextField("Beschreibung zum Modul")
    host = models.CharField("Anbieter des Moduls", max_length=255)
    quota_economics = models.IntegerField("Anteil Wirtschaftswissenschaft", default=0)
    quota_cs = models.IntegerField("Anteil Informatik", default=0)
    quota_is = models.IntegerField("Anteil Wirtschaftsinformatik", default=0)
    quota_key_competence = models.IntegerField("Anteil Schlüsselkompetenz", default=0)
    ects = models.IntegerField("ECTS Punkte", default=0)
    TermType = models.TextChoices("TermType", "SS WS SS/WS")
    term = models.CharField(choices=TermType.choices, max_length=5, default=TermType.SS)

    def __str__(self):
        return self.title


class TermStarts(datetime.date, models.Choices):
    WS_18 = 2018, 10, 1, "Wintersemester 2018/19"
    SS_19 = 2019, 4, 1, "Sommersemester 2019"
    WS_19 = 2019, 10, 1, "Wintersemester 2019/20"
    SS_20 = 2020, 4, 1, "Sommersemester 2020"
    WS_20 = 2020, 10, 1, "Wintersemester 2020/21"
    SS_21 = 2021, 4, 1, "Sommersemester 2021"
    WS_21 = 2021, 10, 1, "Wintersemester 2021/22"


class SemesterModule(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="semester_modules",
    )
    module = models.ForeignKey(
        Module,
        verbose_name="Modulbezeichnung",
        on_delete=models.SET_NULL,
        null=True,
        related_name="semester_modules",
    )
    term = models.DateField(choices=TermStarts.choices, verbose_name="Semester")
    points_sl = models.FloatField(
        "Punkte Studienleistung",
        validators=[MinValueValidator(0.0), MaxValueValidator(18)],
        null=True,
        blank=True,
    )
    points_exam = models.FloatField(
        "Punkte Klausur",
        validators=[MinValueValidator(0.0), MaxValueValidator(90)],
        null=True,
        blank=True,
    )
    grade = models.FloatField(
        "Note",
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)],
        null=True,
        blank=True,
    )
    done = models.BooleanField("Erledigt?", default=False)

    @property
    def last_three_events(self):
        return Event.open_objects.filter(semestermodule=self.pk)[:3]

    class Meta:
        ordering = ["term"]

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        """Return absolute url to the semestermodule detail page."""
        return reverse("terms:detail", kwargs={"pk": self.pk})


class OpenEventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(done=False)


class Event(TimeStampedModel):
    class EventType(models.TextChoices):
        SCRIPT = "SC", _("Skriptbearbeitung")
        SL = "SL", _("Studienleistung")
        EXAM_A = "EA", _("Klausur Block A")
        EXAM_B = "EB", _("Klausur Block B")
        EXAM_C = "EC", _("Klausur Block C")
        ALIGNMENT = "AL", _("Abstimmungstermin")

    semestermodule = models.ForeignKey(
        SemesterModule, on_delete=models.CASCADE, related_name="events"
    )
    title = models.CharField("Bezeichnung", max_length=255)
    start_date = models.DateTimeField("Start des Ereignisses")
    end_date = models.DateTimeField("Ende des Ereignisses", blank=True, null=True)
    event_type = models.CharField(
        max_length=2,
        choices=EventType.choices,
        default=EventType.SCRIPT,
    )
    note = models.TextField("Notiz", blank=True)
    done = models.BooleanField("Erledigt?", default=False)
    done_at = models.DateTimeField("Erledigt am", blank=True, null=True)

    @property
    def all_day(self):
        if self.end_date:
            delta = self.end_date - self.start_date
            if delta.days > 0:
                return True
        else:
            return False

    objects = models.Manager()
    open_objects = OpenEventManager()

    class Meta:
        ordering = ["start_date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Return absolute url to the events detail page."""
        return reverse(
            "terms:detail_event",
            kwargs={"pk": self.pk, "semestermodule_id": self.semestermodule_id},
        )
