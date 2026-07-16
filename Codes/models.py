cat > extra/Codes/Codes/models.py << 'EOF'
from django.db import models
from bd_models.models import Ball, Special

class RedeemCode(models.Model):
    code = models.CharField(max_length=50, unique=True, help_text="The code players will type")
    ball = models.ForeignKey(Ball, on_delete=models.CASCADE, help_text="Ball reward")
    special = models.ForeignKey(Special, on_delete=models.SET_NULL, null=True, blank=True, help_text="Optional special")
    expires_at = models.DateTimeField(null=True, blank=True, help_text="Leave empty if never expires")
    max_uses = models.PositiveIntegerField(default=1, help_text="How many times this code can be used")
    current_uses = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Redeem Code"
        verbose_name_plural = "Redeem Codes"
EOF
