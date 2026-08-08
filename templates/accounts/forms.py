from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=[
            (User.Role.MEMBER, "Member"),
            (User.Role.PASTOR, "Pastor"),
            (User.Role.SECRETARY, "Secretary"),
            (User.Role.FINANCE_OFFICER, "Finance Officer"),
        ],
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'role')


class StaffUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'role', 'branch')