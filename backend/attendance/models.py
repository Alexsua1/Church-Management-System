from django.db import models
from backend.members.models import Member
from backend.accounts.models import Branch
from backend.events.models import Event


class AttendanceSession(models.Model):
    """A single attendance-taking session, e.g. Sunday Service, Bible Study, or a specific Event."""
    class SessionType(models.TextChoices):
        SUNDAY_SERVICE = "SUNDAY_SERVICE", "Sunday Service"
        BIBLE_STUDY = "BIBLE_STUDY", "Bible Study"
        PRAYER_MEETING = "PRAYER_MEETING", "Prayer Meeting"
        EVENT = "EVENT", "Event"
        OTHER = "OTHER", "Other"

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="attendance_sessions")
    session_type = models.CharField(max_length=20, choices=SessionType.choices, default=SessionType.SUNDAY_SERVICE)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True, related_name="attendance_sessions")
    date = models.DateField()
    qr_token = models.CharField(max_length=64, unique=True, blank=True, null=True,
                                 help_text="Token embedded in the QR code for self check-in.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_session_type_display()} - {self.date}"


class AttendanceRecord(models.Model):
    class CheckInMethod(models.TextChoices):
        MANUAL = "MANUAL", "Manual"
        QR_CODE = "QR_CODE", "QR Code"

    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name="records")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="attendance_records")
    check_in_time = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=10, choices=CheckInMethod.choices, default=CheckInMethod.MANUAL)

    class Meta:
        unique_together = ("session", "member")

    def __str__(self):
        return f"{self.member} @ {self.session}"
