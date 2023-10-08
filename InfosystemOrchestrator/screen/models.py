from django.db import models
from django.db.models import RESTRICT


# Create your models here.


class ScreenCommand(models.Model):
    command_name = models.CharField(max_length=255)

    base_command = models.CharField(max_length=255)
    args = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.pk} - {self.command_name}"


class AutomaticScreenSwitcher(models.Model):
    profile_name = models.CharField(max_length=255)

    command_list = models.ManyToManyField(ScreenCommand, blank=True)
    change_time = models.IntegerField(default=60)
    randomise = models.BooleanField(default=False)

    current_command = models.ForeignKey(ScreenCommand, blank=True, null=True, on_delete=RESTRICT, related_name='current_screen_command')


class ScreenGroup(models.Model):
    name = models.CharField(max_length=255)
    assigned_command = models.ForeignKey(ScreenCommand, null=True, blank=True, on_delete=RESTRICT)

    switching_mode = models.ForeignKey(AutomaticScreenSwitcher, null=True, blank=True, on_delete=RESTRICT)

    @property
    def command(self):
        if self.switching_mode:
            return self.switching_mode.current_command
        else:
            return self.assigned_command

    def __str__(self):
        return f"{self.pk} - {self.name}"


class Screen(models.Model):
    name = models.CharField(max_length=255)
    passphrase = models.CharField(max_length=255)
    last_connected_at = models.DateTimeField(null=True, blank=True, default=None)

    screen_group = models.ForeignKey(ScreenGroup, null=True, blank=True, on_delete=RESTRICT)
    overriden_current_command = models.ForeignKey(ScreenCommand, null=True, blank=True, on_delete=RESTRICT)

    @property
    def command(self):
        if self.overriden_current_command:
            return self.overriden_current_command
        elif self.screen_group and self.screen_group.assigned_command:
            return self.screen_group.assigned_command
        return None

    def __str__(self):
        return f"{self.pk} - {self.name}"
