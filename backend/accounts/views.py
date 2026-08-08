from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import LoginForm, StaffUserCreationForm
from .decorators import admin_required


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        if user is not None:
            login(request, user)
            return redirect('dashboard:home')
        messages.error(request, "Invalid username or password.")
    return render(request, "accounts/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('public:home')


@admin_required
def manage_users(request):
    from .models import User
    users = User.objects.all().order_by("role", "username")
    return render(request, "accounts/user_list.html", {"users": users})


@admin_required
def create_user(request):
    form = StaffCustomUserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New user account created.")
        return redirect('accounts:manage_users')
    return render(request, "accounts/user_form.html", {"form": form})


@login_required
def profile(request):
    return render(request, "accounts/profile.html", {"user_obj": request.user})
from django.shortcuts import render, redirect
from.forms import UserCreationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form =UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login') # Replace with your login URL name
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

