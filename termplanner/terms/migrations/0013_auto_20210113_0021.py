# Generated by Django 3.0.11 on 2021-01-12 23:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terms', '0012_auto_20201229_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semestermodule',
            name='points_exam',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(90)], verbose_name='Punkte Klausur'),
        ),
        migrations.AlterField(
            model_name='semestermodule',
            name='points_sl',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(18)], verbose_name='Punkte Studienleistung'),
        ),
    ]