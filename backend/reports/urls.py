from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path('', views.report_center, name='center'),
    path('members/excel/', views.export_members_excel, name='members_excel'),
    path('finance/pdf/', views.export_finance_pdf, name='finance_pdf'),
    path('attendance/excel/', views.export_attendance_excel, name='attendance_excel'),
]
