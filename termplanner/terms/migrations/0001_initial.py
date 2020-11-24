# Generated by Django 3.0.11 on 2020-11-24 22:26

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='Titel des Moduls')),
                ('short_title', models.CharField(max_length=5, verbose_name='Abkürzung des Moduls')),
                ('description', models.TextField(verbose_name='Beschreibung zum Modul')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
