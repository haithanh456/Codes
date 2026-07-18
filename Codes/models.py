from django.db import models

class RedeemCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    reward = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Redeem Code"
        verbose_name_plural = "Redeem Codes"
