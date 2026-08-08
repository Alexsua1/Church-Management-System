from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path('', views.event_list, name='list'),
    path('add/', views.event_create, name='create'),
    path('announcements/', views.announcement_list, name='announcements'),
    path('announcements/add/', views.announcement_create, name='announcement_create'),
]
