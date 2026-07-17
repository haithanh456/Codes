cat > extra/Codes/Codes/models.py << 'EOF'
from django.db import models
from bd_models.models import Ball, Special

class RedeemCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    ball = models.ForeignKey(Ball, on_delete=models.SET_NULL, null=True, blank=True)
    special = models.ForeignKey(Special, on_delete=models.SET_NULL, null=True, blank=True)
    currency_amount = models.PositiveIntegerField(default=0)
    expires_at = models.DateTimeField(null=True, blank=True)
    max_uses = models.PositiveIntegerField(default=1)
    current_uses = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Redeem Code"
        verbose_name_plural = "Redeem Codes"
EOF
