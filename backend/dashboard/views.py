from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta

from backend.members.models import Member
from backend.finance.models import Offering, Expense
from backend.attendance.models import AttendanceRecord, AttendanceSession
from backend.events.models import Event, Announcement
from backend.departments.models import Department


@login_required
def home(request):
    user = request.user
    today = timezone.now().date()
    context = {"today": today}

    total_members = Member.objects.filter(status="ACTIVE").count()
    context["total_members"] = total_members
    context["total_departments"] = Department.objects.count()
    context["upcoming_events"] = Event.objects.filter(start_datetime__gte=timezone.now()).order_by("start_datetime")[:5]
    context["recent_announcements"] = Announcement.objects.order_by("-created_at")[:5]

    if user.is_admin() or user.is_pastor():
        last_session = AttendanceSession.objects.order_by("-date").first()
        context["last_attendance_count"] = last_session.records.count() if last_session else 0
        context["last_session"] = last_session

    if user.is_admin() or user.is_finance_officer():
        month_start = today.replace(day=1)
        context["month_offerings_total"] = sum(
            o.amount for o in Offering.objects.filter(date__gte=month_start)
        )
        context["month_expenses_total"] = sum(
            e.amount for e in Expense.objects.filter(date__gte=month_start)
        )

    template_map = {
        "ADMIN": "dashboard/admin_dashboard.html",
        "PASTOR": "dashboard/pastor_dashboard.html",
        "SECRETARY": "dashboard/secretary_dashboard.html",
        "FINANCE_OFFICER": "dashboard/finance_dashboard.html",
    }
    template = template_map.get(user.role, "dashboard/member_dashboard.html")
    if user.is_superuser:
        template = "dashboard/admin_dashboard.html"

    return render(request, template, context)
