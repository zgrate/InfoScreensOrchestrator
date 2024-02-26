from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from screen.models import Screen
from screen.serializers import ScreenSerializer


# Create your views here.
@api_view(['GET'])
def screen_view(request, passphrase=None):
    screen = Screen.objects.filter(passphrase=passphrase).first()
    if screen:
        serializer = ScreenSerializer(instance=screen)

        return Response(data=serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': "Invalid screen passphrase"})


@api_view(['POST'])
def generate_screen(request, name=None):
    screen = Screen.objects.get_or_create(name=name)[0]
    return Response(data={"name": name, "passphrase": screen.passphrase})