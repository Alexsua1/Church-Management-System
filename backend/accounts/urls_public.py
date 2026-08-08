from django.urls import path
from . import views_public as views

app_name = "public"

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('events/', views.public_events, name='events'),
    path('donate/', views.donate, name='donate'),
    path('donate/callback/', views.donate_callback, name='donate_callback'),
    path('donate/webhook/', views.paystack_webhook, name='paystack_webhook'),
]
