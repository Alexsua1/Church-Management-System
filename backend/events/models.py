from django.db import models
from backend.accounts.models import Branch


class Event(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    banner_image = models.ImageField(upload_to="event_banners/", blank=True, null=True)
    is_public = models.BooleanField(default=True, help_text="Show on the public Events page.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_datetime"]

    def __str__(self):
        return self.title


class Announcement(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="announcements")
    title = models.CharField(max_length=200)
    message = models.TextField()
    posted_by = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, related_name="announcements")
    send_sms = models.BooleanField(default=False)
    send_whatsapp = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
