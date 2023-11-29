from rest_framework import serializers

from healthcheck.models import DeviceBeatModel


class BeatCreateSerializer(serializers.ModelSerializer):
    data = serializers.JSONField(allow_null=True)

    def create(self, validated_data):
        from screen.models import Screen
        device = Screen.objects.filter(validated_data['used_passphrase']).first()
        if device is None:
            device_name = "Device Not Found"
        else:
            device_name = device.name
        validated_data['device_name'] =
        DeviceBeatModel.objects.create(**)

    class Meta:
        model = DeviceBeatModel
        fields = ['created_at', 'device_name', 'used_passphrase', 'data']
