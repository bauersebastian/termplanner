from django import forms
from tempus_dominus.widgets import DateTimePicker

from .models import Event


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
