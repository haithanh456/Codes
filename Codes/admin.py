from django.contrib import admin
from .models import RedeemCode

@admin.register(RedeemCode)
class RedeemCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "reward_type", "ball", "special", "currency_amount", "expires_at", "current_uses", "max_uses", "is_active")
    list_filter = ("reward_type", "is_active")
    search_fields = ("code",)
    list_editable = ("is_active",)
    autocomplete_fields = ("ball", "special")

    fieldsets = (
        (None, {
            "fields": ("code", "reward_type", "is_active")
        }),
        ("Countryball Reward", {
            "fields": ("ball", "special"),
        }),
        ("Coins Reward", {
            "fields": ("currency_amount",),
        }),
        ("Limits", {
            "fields": ("expires_at", "max_uses", "current_uses")
        }),
    )
