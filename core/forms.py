from django import forms

from .models import Activity, ActivityInstance


class ActivityForm(forms.ModelForm):

    class Meta:
        model = Activity
        fields = (
            "title",
            "type",
            "description",
        )
        labels = {
            "description": "Description (optional) - e.g. state why you want to track this activity"
        }


class TrackerForm(forms.ModelForm):
    class Meta:
        model = ActivityInstance
        fields = (
            "activity",
            "start_time",
            "end_time",
            "duration",
        )
