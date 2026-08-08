from django import forms
from .models import AttendanceSession


class SessionForm(forms.ModelForm):
    class Meta:
        model = AttendanceSession
        fields = ["branch", "session_type", "event", "date"]
        widgets = {
            "branch": forms.Select(attrs={"class": "form-select"}),
            "session_type": forms.Select(attrs={"class": "form-select"}),
            "event": forms.Select(attrs={"class": "form-select"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }
