from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Department
from .forms import DepartmentForm
from backend.accounts.decorators import staff_required


@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, "departments/department_list.html", {"departments": departments})


@login_required
def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    return render(request, "departments/department_detail.html", {"department": department})


@staff_required
def department_create(request):
    form = DepartmentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Department created.")
        return redirect('departments:list')
    return render(request, "departments/department_form.html", {"form": form})
