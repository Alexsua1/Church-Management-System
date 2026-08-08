from django import forms
from .models import Department


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "branch": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "leader_name": forms.TextInput(attrs={"class": "form-control"}),
            "leader_phone": forms.TextInput(attrs={"class": "form-control"}),
        }
