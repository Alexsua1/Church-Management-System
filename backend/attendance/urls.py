from django.urls import path
from . import views

app_name = "attendance"

urlpatterns = [
    path('', views.session_list, name='list'),
    path('new/', views.session_create, name='create'),
    path('<int:pk>/take/', views.take_attendance, name='take'),
    path('checkin/<str:token>/', views.qr_checkin, name='qr_checkin'),
]
