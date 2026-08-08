import hashlib
import hmac
import json
import uuid
import requests
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactForm, DonationForm
from backend.events.models import Event
from backend.finance.models import Offering

PAYSTACK_BASE_URL = "https://api.paystack.co"


def home(request):
    upcoming_events = Event.objects.filter(is_public=True, start_datetime__gte=timezone.now()).order_by("start_datetime")[:3]
    return render(request, "public/home.html", {"upcoming_events": upcoming_events})


def about(request):
    return render(request, "public/about.html")


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        # Hook up an email backend or SMS/WhatsApp notification here.
        messages.success(request, "Thank you! Your message has been received. We will get back to you soon.")
        return redirect('public:contact')
    return render(request, "public/contact.html", {"form": form})


def public_events(request):
    events = Event.objects.filter(is_public=True).order_by("-start_datetime")
    return render(request, "public/events.html", {"events": events})


def donate(request):
    form = DonationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if not settings.PAYSTACK_SECRET_KEY:
            messages.error(request, "Online giving isn't configured yet. Please add your Paystack "
                                     "secret key to the .env file (PAYSTACK_SECRET_KEY).")
            return render(request, "public/donate.html", {"form": form})

        amount = form.cleaned_data["amount"]
        email = form.cleaned_data["email"] or "donor@oforikromcentral.church"
        donor_name = form.cleaned_data["donor_name"] or "Anonymous"
        offering_type = form.cleaned_data["offering_type"]
        reference = f"COP-{uuid.uuid4().hex[:12].upper()}"

        callback_url = request.build_absolute_uri(reverse('public:donate_callback'))

        try:
            response = requests.post(
                f"{PAYSTACK_BASE_URL}/transaction/initialize",
                headers={"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"},
                json={
                    "email": email,
                    "amount": int(amount * 100),  # Paystack expects amount in pesewas/kobo
                    "currency": "GHS",
                    "reference": reference,
                    "callback_url": callback_url,
                    "metadata": {
                        "donor_name": donor_name,
                        "offering_type": offering_type,
                    },
                },
                timeout=15,
            )
            data = response.json()
        except requests.RequestException:
            messages.error(request, "We couldn't reach the payment provider. Please try again shortly.")
            return render(request, "public/donate.html", {"form": form})

        if data.get("status"):
            # Save a PENDING record now so we have a trail even if the donor abandons checkout.
            Offering.objects.create(
                branch_id=1,
                donor_name=donor_name,
                offering_type=offering_type,
                amount=amount,
                payment_method=Offering.PaymentMethod.CARD,
                reference=reference,
                date=timezone.now().date(),
            )
            return redirect(data["data"]["authorization_url"])

        messages.error(request, data.get("message", "Could not start the payment. Please try again."))
        return render(request, "public/donate.html", {"form": form})

    return render(request, "public/donate.html", {"form": form})


def donate_callback(request):
    """Paystack redirects the donor here after checkout. We verify server-side before
    treating the gift as confirmed — never trust the redirect alone."""
    reference = request.GET.get("reference") or request.GET.get("trxref")
    if not reference:
        messages.error(request, "No payment reference found.")
        return redirect('public:donate')

    try:
        response = requests.get(
            f"{PAYSTACK_BASE_URL}/transaction/verify/{reference}",
            headers={"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"},
            timeout=15,
        )
        data = response.json()
    except requests.RequestException:
        messages.error(request, "We couldn't confirm your payment right now. If you were charged, "
                                 "please contact the church office with your reference: " + reference)
        return redirect('public:donate')

    tx = data.get("data", {})
    offering = Offering.objects.filter(reference=reference).first()

    if data.get("status") and tx.get("status") == "success":
        messages.success(request, f"Thank you for your generous giving of GHS {tx.get('amount', 0) / 100:.2f}! "
                                   f"God bless you. (Ref: {reference})")
    else:
        if offering:
            offering.delete()  # payment wasn't completed — don't keep a phantom record
        messages.error(request, "Your payment was not completed. Please try again.")

    return redirect('public:donate')


@csrf_exempt
def paystack_webhook(request):
    """Server-to-server confirmation from Paystack. Configure this URL (yourdomain.com/donate/webhook/)
    in your Paystack dashboard under Settings > API Keys & Webhooks. This is the authoritative
    source of truth for whether a payment succeeded — more reliable than the browser redirect alone."""
    if request.method != "POST":
        return HttpResponse(status=405)

    signature = request.headers.get("x-paystack-signature", "")
    expected = hmac.new(
        settings.PAYSTACK_SECRET_KEY.encode("utf-8"), request.body, hashlib.sha512
    ).hexdigest()
    if not settings.PAYSTACK_SECRET_KEY or not hmac.compare_digest(signature, expected):
        return HttpResponse(status=401)

    event = json.loads(request.body)
    if event.get("event") == "charge.success":
        tx = event.get("data", {})
        reference = tx.get("reference")
        if reference and not Offering.objects.filter(reference=reference).exists():
            metadata = tx.get("metadata", {}) or {}
            Offering.objects.create(
                branch_id=1,
                donor_name=metadata.get("donor_name", "Anonymous"),
                offering_type=metadata.get("offering_type", Offering.OfferingType.DONATION),
                amount=(tx.get("amount", 0) or 0) / 100,
                payment_method=Offering.PaymentMethod.CARD,
                reference=reference,
                date=timezone.now().date(),
            )

    return HttpResponse(status=200)
