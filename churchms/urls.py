from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('backend.accounts.urls_public', namespace='public')),
    path('accounts/', include('backend.accounts.urls', namespace='accounts')),
    path('dashboard/', include('backend.dashboard.urls', namespace='dashboard')),
    path('members/', include('backend.members.urls', namespace='members')),
    path('attendance/', include('backend.attendance.urls', namespace='attendance')),
    path('finance/', include('backend.finance.urls', namespace='finance')),
    path('departments/', include('backend.departments.urls', namespace='departments')),
    path('events/', include('backend.events.urls', namespace='events')),
    path('inventory/', include('backend.inventory.urls', namespace='inventory')),
    path('reports/', include('backend.reports.urls', namespace='reports')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
