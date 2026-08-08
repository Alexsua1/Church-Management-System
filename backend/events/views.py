from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Event, Announcement
from .forms import EventForm, AnnouncementForm
from backend.accounts.decorators import staff_required


@login_required
def event_list(request):
    events = Event.objects.order_by("-start_datetime")
    return render(request, "events/event_list.html", {"events": events})


@staff_required
def event_create(request):
    form = EventForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Event created.")
        return redirect('events:list')
    return render(request, "events/event_form.html", {"form": form})


@login_required
def announcement_list(request):
    announcements = Announcement.objects.order_by("-created_at")
    return render(request, "events/announcement_list.html", {"announcements": announcements})


@staff_required
def announcement_create(request):
    form = AnnouncementForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        announcement = form.save(commit=False)
        announcement.posted_by = request.user
        announcement.save()
        # TODO: if announcement.send_sms / send_whatsapp -> call notification provider here.
        messages.success(request, "Announcement posted.")
        return redirect('events:announcements')
    return render(request, "events/announcement_form.html", {"form": form})
