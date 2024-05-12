from rest_framework import serializers

from screen.models import Screen, ScreenCommand, ScreenGroup


class ScreenCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreenCommand
        fields = ['command_name', 'base_command', 'args']


class ScreenGroupSerializer(serializers.ModelSerializer):
    assigned_command = ScreenCommandSerializer(read_only=True, allow_null=True)
    
    class Meta:
        model = ScreenGroup
        fields = ['name', 'assigned_command']


class ScreenSerializer(serializers.ModelSerializer):
    command = ScreenCommandSerializer(read_only=True, allow_null=True)
    screen_group = ScreenGroupSerializer(read_only=True, allow_null=True)
    background_audio_stream = serializers.CharField(allow_null=True)
    force_override = serializers.BooleanField()

    class Meta:
        model = Screen
        fields = ['name', 'screen_group', 'command', 'background_audio_stream', 'force_override']
