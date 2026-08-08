from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}))


class StaffUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "role", "branch", "phone_number"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "role": forms.Select(attrs={"class": "form-select"}),
            "branch": forms.Select(attrs={"class": "form-select"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})


class ContactForm(forms.Form):
    name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={"class": "form-control"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "rows": 5}))


class DonationForm(forms.Form):
    donor_name = forms.CharField(max_length=150, required=False,
                                  widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Full name (optional)"}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={"class": "form-control"}))
    amount = forms.DecimalField(min_value=1, widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Amount (GHS)"}))
    offering_type = forms.ChoiceField(
        choices=[("TITHE", "Tithe"), ("OFFERING", "General Offering"),
                 ("THANKSGIVING", "Thanksgiving"), ("BUILDING_FUND", "Building Fund"),
                 ("SEED", "Seed / Special Offering")],
        widget=forms.Select(attrs={"class": "form-select"}),
    )

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'role')

