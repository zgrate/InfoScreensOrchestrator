from django.db import models
from django.db.models import RESTRICT
from django.utils import timezone


# Create your models here.


class ScreenCommand(models.Model):
    command_name = models.CharField(max_length=255)

    base_command = models.CharField(max_length=255)
    args = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.pk} - {self.command_name}"


class AutomaticScreenSwitcher(models.Model):
    profile_name = models.CharField(max_length=255)

    change_time_seconds = models.IntegerField(default=60)
    randomise = models.BooleanField(default=False)
    last_switch = models.DateTimeField(null=True, blank=True, default=timezone.now)

    current_command = models.ForeignKey('AutomaticCommand', blank=True, null=True, on_delete=RESTRICT,
                                        related_name='current_screen_command')

    def __str__(self):
        return f"ScreenSwitcher {self.profile_name}"


class AutomaticCommand(models.Model):
    screen_switcher = models.ForeignKey(AutomaticScreenSwitcher, on_delete=RESTRICT, related_name='automatic_commands')
    command = models.ForeignKey(ScreenCommand, on_delete=RESTRICT)
    number_order = models.IntegerField()

    def __str__(self):
        return f"Command {self.number_order} for screen {self.screen_switcher.profile_name} with id {self.command.command_name}"

    class Meta:
        unique_together = ('screen_switcher', 'number_order')


class ScreenGroup(models.Model):
    name = models.CharField(max_length=255)
    assigned_command = models.ForeignKey(ScreenCommand, null=True, blank=True, on_delete=RESTRICT)

    switching_mode = models.ForeignKey(AutomaticScreenSwitcher, null=True, blank=True, on_delete=RESTRICT, related_name='switching_screens_group')

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
