from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response

from printingserver.consumers import PrintingServiceWebsocket
from printingserver.forms import UploadForm


# Create your views here.
@api_view(["GET", "POST"])
def upload_form(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return redirect("/admin/login/?next=/upload_form/")
        else:
            return render(request, "upload_form.html", context={
                'user': request.user.username,
                'form': UploadForm()
            })
    elif request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        form.instance.user_id = request.user.id

        if not form.is_valid():
            return render(request, "upload_form.html", context={"error_message": form.errors})
        else:
            form.save()
            return render(request, "upload_form.html", context={"success_message": "Success!"})


def notification_receiver(request):
    if not request.user.is_authenticated:
        return redirect("/admin/login/?next=/notification_receiver/")
    else:
        return render(request, "notification_receiver.html")


@api_view(['GET'])
def test_call(request):
    async_to_sync(get_channel_layer().group_send)(settings.PRINTING_SERVICE_GROUP,
                                                  {"type": "system.message", "message": "Bajo jajo"})
    return Response(status=200, data={"yes": "no"})
