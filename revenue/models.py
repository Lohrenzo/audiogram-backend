from django.db import models
from django.conf import settings

from api.models import Audio


class StreamRecord(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="stream_user",
    )
    audio = models.ForeignKey(Audio, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "StreamRecords"


class Subscription(models.Model):
    options = (
        ("student", "Student"),
        ("premium", "Premium"),
    )

    amount = models.BigIntegerField(default=0)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscription_user",
    )
    status = models.CharField(
        max_length=10,
        choices=options,
        default="premium",
    )

    class Meta:
        verbose_name_plural = "Subscriptions"
