import datetime

from django.db import models
from model_utils.models import TimeStampedModel

# from django.urls import reverse
# from autoslug import AutoSlugField
# from django.conf import settings


class Module(TimeStampedModel):
    title = models.CharField("Titel des Moduls", max_length=255)
    short_title = models.CharField("Abkürzung des Moduls", max_length=5)
    description = models.TextField("Beschreibung zum Modul")


class TermStarts(datetime.date, models.Choices):
    WS_20 = 2020, 10, 1, "Wintersemester 2020/21"
    SS_21 = 2021, 4, 1, "Sommersemester 2021"
    WS_21 = 2021, 10, 1, "Wintersemester 2021/22"
    SS_22 = 2022, 4, 1, "Sommersemester 2022"
    WS_22 = 2022, 10, 1, "Wintersemester 2022/23"
    SS_23 = 2023, 4, 1, "Sommersemester 2023"


"""
class Term(TimeStampedModel):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    year = models.DateField(choices=TermStarts.choices)
"""


"""
class Event(TimeStampedModel):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
"""
