from django.db import models


class Department(models.Model):
    """e.g. Choir, Ushers, Youth Ministry, Men's Fellowship, Women's Fellowship."""
    name = models.CharField(max_length=150)
    branch = models.ForeignKey("accounts.Branch", on_delete=models.CASCADE, related_name="departments")
    description = models.TextField(blank=True)
    leader_name = models.CharField(max_length=150, blank=True)
    leader_phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("name", "branch")

    def __str__(self):
        return self.name
