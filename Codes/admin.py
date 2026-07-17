cat > extra/Codes/Codes/admin.py << 'EOF'
from django.contrib import admin
from .models import RedeemCode

@admin.register(RedeemCode)
class RedeemCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "ball", "special", "currency_amount", "expires_at", "current_uses", "max_uses", "is_active")
    list_filter = ("is_active",)
    search_fields = ("code",)
    list_editable = ("is_active",)
    autocomplete_fields = ("ball", "special")
EOF
