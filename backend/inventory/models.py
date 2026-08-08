from django.db import models
from backend.accounts.models import Branch


class InventoryItem(models.Model):
    class Condition(models.TextChoices):
        NEW = "NEW", "New"
        GOOD = "GOOD", "Good"
        FAIR = "FAIR", "Fair"
        NEEDS_REPAIR = "NEEDS_REPAIR", "Needs Repair"
        DISPOSED = "DISPOSED", "Disposed"

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="inventory_items")
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=100, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    condition = models.CharField(max_length=20, choices=Condition.choices, default=Condition.GOOD)
    location = models.CharField(max_length=150, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.quantity})"
