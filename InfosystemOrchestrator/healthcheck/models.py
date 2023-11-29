from django.db import models


# Create your models here.

class DeviceBeatModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    device_name = models.CharField(max_length=255, null=True, blank=True)
    used_passphrase = models.CharField(max_length=255, null=True, blank=True)

    data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"DeviceBeat {self.created_at} {self.device_name}"
