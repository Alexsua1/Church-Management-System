from django.contrib import admin
from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("membership_id", "full_name_display", "gender", "phone_number", "branch", "status")
    list_filter = ("branch", "status", "gender", "baptized")
    search_fields = ("first_name", "last_name", "membership_id", "phone_number")

    def full_name_display(self, obj):
        return obj.full_name
    full_name_display.short_description = "Full Name"
