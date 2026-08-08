from django import forms
from .models import Event, Announcement


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ["created_at"]
        widgets = {
            "branch": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "start_datetime": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "end_datetime": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "banner_image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "is_public": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        exclude = ["posted_by", "created_at"]
        widgets = {
            "branch": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "send_sms": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "send_whatsapp": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
