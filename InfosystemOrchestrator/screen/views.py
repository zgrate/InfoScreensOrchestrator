from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from screen.models import Screen, AccessToken, ScreenGroup, ScreenCommand
from screen.serializers import ScreenSerializer, ScreenGroupSerializer
from django.http import HttpResponse

import datetime

last_requests = {
    
}

# Create your views here.
@api_view(['GET'])
def screen_view(request, passphrase=None):
    screen = Screen.objects.filter(passphrase=passphrase).first()
    if screen:
        last_requests[screen.id] = datetime.datetime.now()
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

@api_view(["GET"])
def metrics(request):
    screens = Screen.objects.all()
    groups = ScreenGroup.objects.all()
    now = datetime.datetime.now()
    response = [
        *[f'screens_request_last10s{{name="{screen.name.replace(" ", "_")}", id="{screen.id}"}} {int(now - last_requests.get(screen.id, datetime.datetime.fromtimestamp(0)) <= datetime.timedelta(seconds=10))}' for screen in screens],
        f'screens_available {len(screens)}',
        f'groups_available {len(groups)}',
        *[f'screens_screen_command{{name="{screen.name}", id="{screen.id}", command="{screen.command.command_name.replace(" ", "_")}"}} 1' for screen in screens],
        *[f'screens_screen_group{{name="{screen.name}", id="{screen.id}", group="{screen.screen_group.name.replace(" ", "_")}"}} 1' for screen in screens],
        *[f'screens_screen_group_command{{name="{group.name}", id="{group.id}", command="{group.command.name.replace(" ", "_")}"}} 1' for group in groups]
    ]
    return HttpResponse("\n".join(response), content_type="text/plain")
    
# api_http_requests_total{method="POST", handler="/messages"}

        # 
        # *[f'screens_screen_group{{name="{screen.name}", id="{screen.id}"}} "{screen.screen_group.name}"' for screen in screens],
        # ,