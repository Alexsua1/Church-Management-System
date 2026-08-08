from django.urls import path
from . import views

app_name = "finance"

urlpatterns = [
    path('', views.finance_dashboard, name='dashboard'),
    path('offerings/', views.offering_list, name='offerings'),
    path('offerings/add/', views.offering_create, name='offering_create'),
    path('expenses/', views.expense_list, name='expenses'),
    path('expenses/add/', views.expense_create, name='expense_create'),
    path('expenses/<int:pk>/approve/', views.expense_approve, name='expense_approve'),
]
