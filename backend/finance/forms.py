from django import forms
from .models import Offering, Expense


class OfferingForm(forms.ModelForm):
    class Meta:
        model = Offering
        exclude = ["recorded_by", "created_at"]
        widgets = {
            "branch": forms.Select(attrs={"class": "form-select"}),
            "member": forms.Select(attrs={"class": "form-select"}),
            "donor_name": forms.TextInput(attrs={"class": "form-control"}),
            "offering_type": forms.Select(attrs={"class": "form-select"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
            "payment_method": forms.Select(attrs={"class": "form-select"}),
            "reference": forms.TextInput(attrs={"class": "form-control"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        exclude = ["recorded_by", "created_at", "approved"]
        widgets = {
            "branch": forms.Select(attrs={"class": "form-select"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "receipt": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
