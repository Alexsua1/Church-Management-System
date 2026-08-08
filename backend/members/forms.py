from django import forms
from .models import Member


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        exclude = ["qr_code", "created_at", "updated_at"]
        widgets = {
            "membership_id": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "other_names": forms.TextInput(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-select"}),
            "date_of_birth": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "marital_status": forms.Select(attrs={"class": "form-select"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "residential_address": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "occupation": forms.TextInput(attrs={"class": "form-control"}),
            "branch": forms.Select(attrs={"class": "form-select"}),
            "department": forms.SelectMultiple(attrs={"class": "form-select"}),
            "date_joined": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "baptized": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "photo": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "next_of_kin_name": forms.TextInput(attrs={"class": "form-control"}),
            "next_of_kin_phone": forms.TextInput(attrs={"class": "form-control"}),
        }
