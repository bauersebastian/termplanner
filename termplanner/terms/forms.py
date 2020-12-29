from django import forms
from tempus_dominus.widgets import DateTimePicker

from .models import Event, Module, SemesterModule


class SemesterModuleForm(forms.ModelForm):
    class Meta:
        model = SemesterModule
        fields = ("term", "module", "points_sl", "points_exam", "grade", "done")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["module"].queryset = Module.objects.none()


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
