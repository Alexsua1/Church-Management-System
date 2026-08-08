from django.contrib import admin
from .models import Offering, Expense


@admin.register(Offering)
class OfferingAdmin(admin.ModelAdmin):
    list_display = ("offering_type", "amount", "member", "donor_name", "date", "branch")
    list_filter = ("offering_type", "payment_method", "branch")


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("description", "category", "amount", "date", "approved", "branch")
    list_filter = ("category", "approved", "branch")
