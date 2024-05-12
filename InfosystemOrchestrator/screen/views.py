from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from screen.models import Screen, AccessToken, ScreenGroup, ScreenCommand
from screen.serializers import ScreenSerializer, ScreenGroupSerializer


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
    screen = Screen(name=name)
    screen.save()
    return Response(data={"name": name, "passphrase": screen.passphrase})


@api_view(['GET'])
def switch_command_group(request, access_token, group, new_command):
    if not AccessToken.objects.filter(token=access_token).exists():
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if not (group := ScreenGroup.objects.filter(id=group).first()):
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Invalid ScreenGroup"})

    if not (command := ScreenCommand.objects.filter(id=new_command).first()):
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Invalid Command"})

    group.assigned_command = command
    group.save()
    return Response(data={"status": "ok", "new_command": command.command_name, "screens": group.name})


@api_view(['GET'])
def switch_command_screen(request, access_token, screen_id, new_command):
    if not AccessToken.objects.filter(token=access_token).exists():
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if not (screen := Screen.objects.filter(id=screen_id).first()):
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Invalid screen"})

    if not (command := ScreenCommand.objects.filter(id=new_command).first()):
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Invalid Command"})

    screen.overriden_current_command = command
    screen.save()
    return Response(data={"status": "ok", "new_command": command.command_name, "screen": screen.name})


@api_view(['GET'])
def switch_screen_override(request, access_token, screen_id):
    if not AccessToken.objects.filter(token=access_token).exists():
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if not (screen := Screen.objects.filter(id=screen_id).first()):
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Invalid ScreenGroup"})

    screen.force_override = not screen.force_override
    screen.save()
    return Response(data={"status": "ok", "override_State": screen.force_override, "screen": screen.name})


@api_view(['GET'])
def screen_info(request, access_token, screen_id):
    if not AccessToken.objects.filter(token=access_token).exists():
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if not (screen := Screen.objects.filter(id=screen_id).first()):
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Invalid Screen"})

    return Response(data={"status": "ok", "screen": ScreenSerializer(instance=screen).data})


@api_view(['GET'])
def screen_group_info(request, access_token, screen_group_id):
    if not AccessToken.objects.filter(token=access_token).exists():
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if not (screen := ScreenGroup.objects.filter(id=screen_group_id).first()):
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Invalid ScreenGroup"})

    return Response(data={"status": "ok", "screen_group": ScreenGroupSerializer(instance=screen).data})
