import io
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import qrcode

from .models import Member
from .forms import MemberForm
from backend.accounts.decorators import staff_required


@login_required
def member_list(request):
    query = request.GET.get("q", "")
    members = Member.objects.all()
    if query:
        members = members.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) |
            Q(membership_id__icontains=query) | Q(phone_number__icontains=query)
        )
    return render(request, "members/member_list.html", {"members": members, "query": query})


@login_required
def member_detail(request, pk):
    member = get_object_or_404(Member, pk=pk)
    return render(request, "members/member_detail.html", {"member": member})


@staff_required
def member_create(request):
    form = MemberForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        member = form.save()
        _generate_qr(member)
        messages.success(request, f"Member {member.full_name} registered successfully.")
        return redirect('members:detail', pk=member.pk)
    return render(request, "members/member_form.html", {"form": form, "title": "Register Member"})


@staff_required
def member_update(request, pk):
    member = get_object_or_404(Member, pk=pk)
    form = MemberForm(request.POST or None, request.FILES or None, instance=member)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Member information updated.")
        return redirect('members:detail', pk=member.pk)
    return render(request, "members/member_form.html", {"form": form, "title": "Update Member"})


@staff_required
def member_delete(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == "POST":
        member.delete()
        messages.success(request, "Member record deleted.")
        return redirect('members:list')
    return render(request, "members/member_confirm_delete.html", {"member": member})


def _generate_qr(member):
    """Generate a QR code encoding the member's ID, used for QR-code attendance check-in."""
    qr_img = qrcode.make(f"MEMBER:{member.membership_id}")
    buffer = io.BytesIO()
    qr_img.save(buffer, format="PNG")
    member.qr_code.save(f"{member.membership_id}_qr.png", ContentFile(buffer.getvalue()), save=True)
