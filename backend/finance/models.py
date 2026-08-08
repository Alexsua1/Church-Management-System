from django.db import models
from backend.members.models import Member
from backend.accounts.models import Branch, User


class Offering(models.Model):
    class OfferingType(models.TextChoices):
        TITHE = "TITHE", "Tithe"
        OFFERING = "OFFERING", "General Offering"
        THANKSGIVING = "THANKSGIVING", "Thanksgiving"
        BUILDING_FUND = "BUILDING_FUND", "Building Fund"
        SEED = "SEED", "Seed / Special Offering"
        DONATION = "DONATION", "Online Donation"

    class PaymentMethod(models.TextChoices):
        CASH = "CASH", "Cash"
        MOBILE_MONEY = "MOBILE_MONEY", "Mobile Money"
        CARD = "CARD", "Card / Online"
        BANK = "BANK", "Bank Transfer"

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="offerings")
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name="offerings")
    donor_name = models.CharField(max_length=150, blank=True, help_text="Used for public/anonymous online donations.")
    offering_type = models.CharField(max_length=20, choices=OfferingType.choices, default=OfferingType.OFFERING)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    reference = models.CharField(max_length=100, blank=True, help_text="Payment gateway reference, if any.")
    date = models.DateField()
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="offerings_recorded")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.get_offering_type_display()} - GHS {self.amount} ({self.date})"


class Expense(models.Model):
    class Category(models.TextChoices):
        UTILITIES = "UTILITIES", "Utilities"
        MAINTENANCE = "MAINTENANCE", "Maintenance"
        WELFARE = "WELFARE", "Welfare"
        EVENTS = "EVENTS", "Events"
        ADMIN = "ADMIN", "Administration"
        OTHER = "OTHER", "Other"

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="expenses")
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.OTHER)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    receipt = models.FileField(upload_to="receipts/", blank=True, null=True)
    approved = models.BooleanField(default=False)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="expenses_recorded")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.description} - GHS {self.amount}"
