import datetime

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from model_utils.models import TimeStampedModel

# from autoslug import AutoSlugField


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
    WS_20 = 2020, 10, 1, "Wintersemester 2020/21"
    SS_21 = 2021, 4, 1, "Sommersemester 2021"
    WS_21 = 2021, 10, 1, "Wintersemester 2021/22"
    SS_22 = 2022, 4, 1, "Sommersemester 2022"
    WS_22 = 2022, 10, 1, "Wintersemester 2022/23"
    SS_23 = 2023, 4, 1, "Sommersemester 2023"


class SemesterModule(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True)
    term = models.DateField(choices=TermStarts.choices)
    points_sl = models.FloatField(
        "Punkte Studienleistung",
        validators=[MinValueValidator(0.0), MaxValueValidator(18)],
        default=0,
        null=True,
        blank=True,
    )
    points_exam = models.FloatField(
        "Punkte Klausur",
        validators=[MinValueValidator(0.0), MaxValueValidator(18)],
        default=0,
        null=True,
        blank=True,
    )
    grade = models.FloatField(
        "Note",
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)],
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.module.title

    def get_absolute_url(self):
        """Return absolute url to the trips detail page."""
        return reverse("terms:detail", kwargs={"pk": self.pk})


"""
class Event(TimeStampedModel):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
"""
