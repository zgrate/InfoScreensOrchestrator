import random
import string

import django.conf.global_settings
from django.conf import settings
from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models
from django.db.models import RESTRICT
from django.utils import timezone


# Create your models here.


class ScreenCommand(models.Model):
    command_name = models.CharField(max_length=255)

    base_command = models.CharField(max_length=255)
    args = models.TextField(null=True, blank=True)

    permit_background_audio = models.BooleanField(default=False)

    @classmethod
    def get_default_screen_command(cls):
        return ScreenCommand.objects.get_or_create(command_name='default', defaults={'base_command': 'firefox',
                                                                                     'args': '-kiosk https://zgrate.com/',
                                                                                     'permit_background_audio': True})[
            0]

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
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Command {self.created} for screen {self.screen_switcher.profile_name} with id {self.command.command_name}"

    class Meta:
        ordering = ['created']


class ScreenGroup(models.Model):
    name = models.CharField(max_length=255)
    assigned_command = models.ForeignKey(ScreenCommand, null=True, blank=True, on_delete=RESTRICT)

    switching_mode = models.ForeignKey(AutomaticScreenSwitcher, null=True, blank=True, on_delete=RESTRICT,
                                       related_name='switching_screens_group')

    disabled = models.BooleanField(default=False)

    @property
    def command(self):
        if self.disabled:
            return None
        if self.switching_mode and self.switching_mode.current_command:
            return self.switching_mode.current_command.command
        else:
            return self.assigned_command

    def __str__(self):
        return f"{self.pk} - {self.name}"


class Screen(models.Model):
    name = models.CharField(max_length=255)
    passphrase = models.CharField(max_length=255)
    last_connected_at = models.DateTimeField(null=True, blank=True, default=None)

    screen_group = models.ForeignKey(ScreenGroup, null=True, blank=True, on_delete=RESTRICT)
    force_override = models.BooleanField(default=False)
    overriden_current_command = models.ForeignKey(ScreenCommand, null=True, blank=True, on_delete=RESTRICT)

    background_audio_url = models.CharField(max_length=1024, null=True, blank=True)

    @property
    def background_audio_stream(self):
        if (cmd := self.command) and self.background_audio_url and cmd.permit_background_audio:
            return self.backgroungroupd_audio_url

        return None

    @property
    def command(self):
        if self.force_override and (cmd := self.overriden_current_command):
            return cmd

        if self.screen_group and self.screen_group.disabled and (cmd := self.overriden_current_command):
            return cmd

        elif self.screen_group and (cmd := self.screen_group.command):
            return cmd
        print("DEFAULT")
        return ScreenCommand.get_default_screen_command()

    def save(
            self, *args, **kwargs
    ):
        if self.passphrase is None or self.passphrase == '':
            self.passphrase = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pk} - {self.name}"


class AccessToken(models.Model):
    token = models.CharField(max_length=255)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    def save(
            self, *args, **kwargs
    ):
        if self.token is None or self.token == '':
            self.passphrase = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        super().save(*args, **kwargs)
