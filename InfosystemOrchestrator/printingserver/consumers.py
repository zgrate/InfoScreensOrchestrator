import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.conf import settings

from printingserver.models import StoredDocument


class PrintingServiceWebsocket(WebsocketConsumer):

    def connect(self):
        print("Connected")
        print(self.scope['user'])
        async_to_sync(self.channel_layer.group_add)(settings.PRINTING_SERVICE_GROUP, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(settings.PRINTING_SERVICE_GROUP, self.channel_name)

        pass

    def receive(self, text_data):

        text_data_json = json.loads(text_data)
        type_of_message = text_data_json['type']
        if type_of_message == 'data':
            self.handle_refresh()

        # self.send(text_data=json.dumps({"message": message}))

    def handle_refresh(self):
        self.send(text_data=json.dumps({"type": "data", "queue": StoredDocument.objects.count()}))

    def system_message(self, event):
        print(event)
        print(self.channel_receive)
        self.send(text_data=json.dumps({"message": event['message']}))
