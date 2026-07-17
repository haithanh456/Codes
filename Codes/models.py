from django.db import models

class RedeemCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    reward = models.CharField(max_length=100, help_text="Example: Germany or 500 coins")
    expires_at = models.DateTimeField(null=True, blank=True)
    max_uses = models.PositiveIntegerField(default=1)
    current_uses = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Redeem Code"
        verbose_name_plural = "Redeem Codes"
