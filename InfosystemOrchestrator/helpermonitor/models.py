from django.db import models


# Create your models here.
class HelperModel(models.Model):
    nickname = models.CharField(max_length=255)


class HelperDutyCategoryModel(models.Model):
    name = models.CharField(max_length=255)


class HelperDutyTimeModel(models.Model):
    duty_start = models.DateTimeField()
    duty_end = models.DateTimeField()
    description = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(HelperDutyCategoryModel, on_delete=models.CASCADE)
    helper = models.ForeignKey(HelperModel, on_delete=models.CASCADE)
