from django.db import models
from bd_models.models import Ball, Special

class RedeemCode(models.Model):
    REWARD_TYPE_CHOICES = [
        ("ball", "Countryball"),
        ("ball_special", "Countryball + Special"),
        ("currency", "Coins"),
    ]

    code = models.CharField(max_length=50, unique=True, help_text="The code players will type")
    reward_type = models.CharField(max_length=20, choices=REWARD_TYPE_CHOICES, default="ball")

    ball = models.ForeignKey(Ball, on_delete=models.SET_NULL, null=True, blank=True, help_text="Select the countryball")
    special = models.ForeignKey(Special, on_delete=models.SET_NULL, null=True, blank=True, help_text="Optional special")
    currency_amount = models.PositiveIntegerField(default=0, help_text="Only used if reward type is Coins")

    expires_at = models.DateTimeField(null=True, blank=True, help_text="Leave empty if it never expires")
    max_uses = models.PositiveIntegerField(default=1)
    current_uses = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Redeem Code"
        verbose_name_plural = "Redeem Codes"
