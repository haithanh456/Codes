from django.contrib import admin
from .models import RedeemCode

@admin.register(RedeemCode)
class RedeemCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'reward_type', 'ball', 'special', 'currency_amount', 'is_active', 'current_uses', 'max_uses']
    list_filter = ['is_active', 'reward_type']
    search_fields = ['code']
    list_editable = ['is_active']
    actions = ['activate', 'deactivate']

    def activate(self, request, queryset):
        queryset.update(is_active=True)
    activate.short_description = "Activate selected codes"

    def deactivate(self, request, queryset):
        queryset.update(is_active=False)
    deactivate.short_description = "Deactivate selected codes"
