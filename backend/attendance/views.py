import secrets
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import AttendanceSession, AttendanceRecord
from .forms import SessionForm
from backend.members.models import Member
from backend.accounts.decorators import staff_required


@login_required
def session_list(request):
    sessions = AttendanceSession.objects.order_by("-date")
    return render(request, "attendance/session_list.html", {"sessions": sessions})


@staff_required
def session_create(request):
    form = SessionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        session = form.save(commit=False)
        session.qr_token = secrets.token_urlsafe(16)
        session.save()
        messages.success(request, "Attendance session created.")
        return redirect('attendance:take', pk=session.pk)
    return render(request, "attendance/session_form.html", {"form": form})


@staff_required
def take_attendance(request, pk):
    session = get_object_or_404(AttendanceSession, pk=pk)
    query = request.GET.get("q", "")
    members = Member.objects.filter(status="ACTIVE")
    if query:
        members = members.filter(first_name__icontains=query) | members.filter(last_name__icontains=query) | members.filter(membership_id__icontains=query)
    checked_in_ids = set(session.records.values_list("member_id", flat=True))

    if request.method == "POST":
        member_id = request.POST.get("member_id")
        member = get_object_or_404(Member, pk=member_id)
        AttendanceRecord.objects.get_or_create(session=session, member=member, defaults={"method": "MANUAL"})
        messages.success(request, f"{member.full_name} checked in.")
        return redirect('attendance:take', pk=session.pk)

    return render(request, "attendance/take_attendance.html", {
        "session": session, "members": members[:50], "query": query,
        "checked_in_ids": checked_in_ids, "checked_in_count": len(checked_in_ids),
    })


@csrf_exempt
def qr_checkin(request, token):
    """Endpoint scanned by a member's QR code. Accepts POST {membership_id}."""
    session = get_object_or_404(AttendanceSession, qr_token=token)
    if request.method == "POST":
        membership_id = request.POST.get("membership_id", "").replace("MEMBER:", "")
        try:
            member = Member.objects.get(membership_id=membership_id)
        except Member.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Member not found."}, status=404)
        _, created = AttendanceRecord.objects.get_or_create(
            session=session, member=member, defaults={"method": "QR_CODE"}
        )
        return JsonResponse({
            "status": "success",
            "message": f"Welcome, {member.full_name}!" if created else "Already checked in.",
        })
    return render(request, "attendance/qr_checkin.html", {"session": session})
