from django.db import models
from backend.accounts.models import Branch
from backend.departments.models import Department


class Member(models.Model):
    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"

    class MaritalStatus(models.TextChoices):
        SINGLE = "SINGLE", "Single"
        MARRIED = "MARRIED", "Married"
        DIVORCED = "DIVORCED", "Divorced"
        WIDOWED = "WIDOWED", "Widowed"

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"
        TRANSFERRED = "TRANSFERRED", "Transferred"

    membership_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    other_names = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=1, choices=Gender.choices)
    date_of_birth = models.DateField(null=True, blank=True)
    marital_status = models.CharField(max_length=10, choices=MaritalStatus.choices, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    residential_address = models.TextField(blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="members")
    department = models.ManyToManyField(Department, blank=True, related_name="members")
    date_joined = models.DateField(auto_now_add=False, null=True, blank=True)
    baptized = models.BooleanField(default=False)
    photo = models.ImageField(upload_to="member_photos/", blank=True, null=True)
    qr_code = models.ImageField(upload_to="qr_codes/", blank=True, null=True)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.ACTIVE)
    next_of_kin_name = models.CharField(max_length=150, blank=True)
    next_of_kin_phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.membership_id})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.other_names} {self.last_name}".replace("  ", " ").strip()
