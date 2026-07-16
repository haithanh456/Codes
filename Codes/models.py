from django.db import models
from bd_models.models import Ball, Special

class RedeemCode(models.Model):
    REWARD_TYPE_CHOICES = [
        ("ball", "Countryball"),
        ("ball_special", "Countryball + Special"),
        ("currency", "Currency (Coins)"),
    ]

    code = models.CharField(max_length=50, unique=True, help_text="The code players will type")
    
    reward_type = models.CharField(
        max_length=20,
        choices=REWARD_TYPE_CHOICES,
        default="ball",
        help_text="What type of reward this code gives"
    )

    # For countryball rewards
    ball = models.ForeignKey(Ball, on_delete=models.CASCADE, null=True, blank=True, help_text="Countryball reward")
    special = models.ForeignKey(Special, on_delete=models.SET_NULL, null=True, blank=True, help_text="Special (only if reward type is Countryball + Special)")

    # For currency reward
    currency_amount = models.PositiveIntegerField(default=0, help_text="How many coins to give (only if reward type is Currency)")

    expires_at = models.DateTimeField(null=True, blank=True, help_text="Leave empty if never expires")
    max_uses = models.PositiveIntegerField(default=1, help_text="How many times this code can be used")
    current_uses = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Redeem Code"
        verbose_name_plural = "Redeem Codes"
