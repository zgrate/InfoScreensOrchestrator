from django.shortcuts import render
from rest_framework.generics import CreateAPIView

from healthcheck.serializers import BeatCreateSerializer


# Create your views here.
class BeatAPI(CreateAPIView):
    serializer_class = BeatCreateSerializer


