from django.db import models

class RedeemCode(models.Model):
    REWARD_TYPE_CHOICES = [
        ("ball", "Countryball"),
        ("ball_special", "Countryball + Special"),
        ("currency", "Currency (Coins)"),
    ]

    code = models.CharField(max_length=50, unique=True)
    reward_type = models.CharField(max_length=20, choices=REWARD_TYPE_CHOICES, default="ball")

    ball = models.CharField(max_length=100, blank=True, null=True, help_text="Type the ball name")
    special = models.CharField(max_length=100, blank=True, null=True, help_text="Type the special name")
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
