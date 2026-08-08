from django.db import models
from django.contrib.auth.models import AbstractUser


class Branch(models.Model):
    """Supports multi-branch churches (e.g. Oforikrom Central, other assemblies)."""
    name = models.CharField(max_length=150, unique=True)
    location = models.CharField(max_length=200, blank=True)
    is_headquarters = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrator"
        PASTOR = "PASTOR", "Pastor"
        SECRETARY = "SECRETARY", "Secretary"
        FINANCE_OFFICER = "FINANCE_OFFICER", "Finance Officer"
        MEMBER = "MEMBER", "Member"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
    phone_number = models.CharField(max_length=20, blank=True)
    profile_photo = models.ImageField(upload_to="profile_photos/", blank=True, null=True)
    dark_mode_enabled = models.BooleanField(default=False)

    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    def is_pastor(self):
        return self.role == self.Role.PASTOR

    def is_secretary(self):
        return self.role == self.Role.SECRETARY

    def is_finance_officer(self):
        return self.role == self.Role.FINANCE_OFFICER
