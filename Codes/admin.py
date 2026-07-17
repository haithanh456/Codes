from django.contrib import admin
from .models import RedeemCode

@admin.register(RedeemCode)
class RedeemCodeAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "reward_type",
        "ball",
        "special",
        "currency_amount",
        "expires_at",
        "current_uses",
        "max_uses",
        "is_active",
    )
    list_filter = ("reward_type", "is_active")
    search_fields = ("code",)
    autocomplete_fields = ("ball", "special")   # ← This prevents 500 errors
    list_editable = ("is_active",)

    fieldsets = (
        (None, {
            "fields": ("code", "reward_type", "is_active")
        }),
        ("Countryball Reward", {
            "fields": ("ball", "special"),
            "description": "Only fill these if reward type is Countryball or Countryball + Special"
        }),
        ("Currency Reward", {
            "fields": ("currency_amount",),
            "description": "Only fill this if reward type is Currency"
        }),
        ("Limits", {
            "fields": ("expires_at", "max_uses", "current_uses")
        }),
    )
