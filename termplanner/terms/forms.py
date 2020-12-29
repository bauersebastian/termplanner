from django import forms
from tempus_dominus.widgets import DateTimePicker

from .models import Event, Module, SemesterModule


class SemesterModuleForm(forms.ModelForm):
    class Meta:
        model = SemesterModule
        fields = ("term", "module", "points_sl", "points_exam", "grade", "done")
        help_texts = {"module": "Bitte Semester zuerst auswählen"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["module"].queryset = Module.objects.none()

        if "term" in self.data:
            try:
                # get the selected modules primary key
                module_pk = self.data.get("module")
                # grab information from the db of that module
                module = Module.objects.get(pk=module_pk)
                # get the term of the module
                term = module.term
                self.fields["module"].queryset = Module.objects.filter(
                    term=term
                ).order_by("title")
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields["module"].queryset = Module.objects.filter(
                term=self.instance.module.term
            ).order_by("title")


class EventForm(forms.ModelForm):
    title = forms.CharField(label="Titel")
    note = forms.CharField(widget=forms.Textarea, label="Notiz", required=False)
    start_date = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                "useCurrent": True,
                "collapse": True,
                "format": "DD.MM.YYYY HH:mm",
            },
            attrs={
                "append": "fa fa-calendar",
                "icon_toggle": True,
            },
        ),
        label="Startzeitpunkt",
    )
    end_date = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                "useCurrent": True,
                "collapse": True,
                "format": "DD.MM.YYYY HH:mm",
            },
            attrs={
                "append": "fa fa-calendar",
                "icon_toggle": True,
            },
        ),
        label="Endezeitpunkt",
        required=False,
    )
    done = forms.BooleanField(label="Erledigt?", required=False)
    event_type = forms.ChoiceField(
        label="Art des Ereignisses", choices=Event.EventType.choices
    )

    class Meta:
        model = Event
        fields = ["title", "note", "start_date", "end_date", "done", "event_type"]
