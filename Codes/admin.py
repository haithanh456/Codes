from django.contrib import admin
from .models import RedeemCode

@admin.register(RedeemCode)
class RedeemCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "ball", "special", "currency_amount", "expires_at", "current_uses", "max_uses", "is_active")
    list_filter = ("is_active",)
    search_fields = ("code",)
    list_editable = ("is_active",)
    raw_id_fields = ("ball", "special")   

    fieldsets = (
        (None, {
            "fields": ("code", "is_active")
        }),
        ("Reward", {
            "fields": ("ball", "special", "currency_amount"),
        }),
        ("Limits", {
            "fields": ("expires_at", "max_uses", "current_uses")
        }),
    )
