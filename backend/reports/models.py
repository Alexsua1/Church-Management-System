from django.db import models
from backend.accounts.models import Branch, User


class GeneratedReport(models.Model):
    class ReportType(models.TextChoices):
        MEMBERSHIP = "MEMBERSHIP", "Membership Report"
        ATTENDANCE = "ATTENDANCE", "Attendance Report"
        FINANCE = "FINANCE", "Financial Report"
        DEPARTMENT = "DEPARTMENT", "Department Report"

    class FileFormat(models.TextChoices):
        PDF = "PDF", "PDF"
        EXCEL = "EXCEL", "Excel"

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="reports")
    report_type = models.CharField(max_length=20, choices=ReportType.choices)
    file_format = models.CharField(max_length=10, choices=FileFormat.choices, default=FileFormat.PDF)
    date_from = models.DateField()
    date_to = models.DateField()
    file = models.FileField(upload_to="reports/", blank=True, null=True)
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reports_generated")
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-generated_at"]

    def __str__(self):
        return f"{self.get_report_type_display()} ({self.date_from} to {self.date_to})"
