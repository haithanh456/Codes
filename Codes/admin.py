from django.contrib import admin
from .models import RedeemCode

@admin.register(RedeemCode)
class RedeemCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "reward", "expires_at", "current_uses", "max_uses", "is_active")
    list_filter = ("is_active",)
    search_fields = ("code", "reward")
    list_editable = ("is_active",)
