from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum

from .models import Offering, Expense
from .forms import OfferingForm, ExpenseForm
from backend.accounts.decorators import finance_required


@finance_required
def finance_dashboard(request):
    total_offerings = Offering.objects.aggregate(total=Sum("amount"))["total"] or 0
    total_expenses = Expense.objects.aggregate(total=Sum("amount"))["total"] or 0
    recent_offerings = Offering.objects.order_by("-date")[:10]
    recent_expenses = Expense.objects.order_by("-date")[:10]
    return render(request, "finance/finance_dashboard.html", {
        "total_offerings": total_offerings, "total_expenses": total_expenses,
        "balance": total_offerings - total_expenses,
        "recent_offerings": recent_offerings, "recent_expenses": recent_expenses,
    })


@finance_required
def offering_list(request):
    offerings = Offering.objects.order_by("-date")
    return render(request, "finance/offering_list.html", {"offerings": offerings})


@finance_required
def offering_create(request):
    form = OfferingForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        offering = form.save(commit=False)
        offering.recorded_by = request.user
        offering.save()
        messages.success(request, "Offering/Tithe recorded successfully.")
        return redirect('finance:offerings')
    return render(request, "finance/offering_form.html", {"form": form})


@finance_required
def expense_list(request):
    expenses = Expense.objects.order_by("-date")
    return render(request, "finance/expense_list.html", {"expenses": expenses})


@finance_required
def expense_create(request):
    form = ExpenseForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        expense = form.save(commit=False)
        expense.recorded_by = request.user
        expense.save()
        messages.success(request, "Expense recorded successfully.")
        return redirect('finance:expenses')
    return render(request, "finance/expense_form.html", {"form": form})


@finance_required
def expense_approve(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    expense.approved = True
    expense.save()
    messages.success(request, "Expense approved.")
    return redirect('finance:expenses')
