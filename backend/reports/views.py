import io
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from openpyxl import Workbook
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from backend.accounts.decorators import staff_required
from backend.members.models import Member
from backend.finance.models import Offering, Expense
from backend.attendance.models import AttendanceRecord


@staff_required
def report_center(request):
    return render(request, "reports/report_center.html")


@staff_required
def export_members_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Members"
    ws.append(["Membership ID", "Full Name", "Gender", "Phone", "Branch", "Status", "Date Joined"])
    for m in Member.objects.all():
        ws.append([m.membership_id, m.full_name, m.get_gender_display(), m.phone_number,
                   str(m.branch), m.get_status_display(), str(m.date_joined or "")])
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = "attachment; filename=members_report.xlsx"
    wb.save(response)
    return response


@staff_required
def export_finance_pdf(request):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = [
        Paragraph("The Church of Pentecost - Oforikrom Central", styles["Title"]),
        Paragraph("Financial Report", styles["Heading2"]),
        Paragraph(f"Generated: {timezone.now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"]),
        Spacer(1, 16),
    ]

    data = [["Type", "Amount (GHS)", "Date", "Method"]]
    for o in Offering.objects.order_by("-date")[:100]:
        data.append([o.get_offering_type_display(), f"{o.amount:.2f}", str(o.date), o.get_payment_method_display()])
    table = Table(data, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a1a6c")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
    ]))
    elements.append(table)
    doc.build(elements)

    response = HttpResponse(buffer.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=finance_report.pdf"
    return response


@staff_required
def export_attendance_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Attendance"
    ws.append(["Member", "Session", "Date", "Method", "Check-in Time"])
    for r in AttendanceRecord.objects.select_related("member", "session").order_by("-check_in_time")[:1000]:
        ws.append([r.member.full_name, r.session.get_session_type_display(), str(r.session.date),
                   r.get_method_display(), r.check_in_time.strftime("%Y-%m-%d %H:%M")])
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = "attachment; filename=attendance_report.xlsx"
    wb.save(response)
    return response
