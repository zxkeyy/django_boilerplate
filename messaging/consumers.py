import json
import base64
import secrets
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.files.base import ContentFile
from django.contrib.auth.models import AnonymousUser
from messaging.models import Conversation, Message
from messaging.serializers import MessageSerializer

def _is_authenticated(self):
    if hasattr(self.scope, 'auth_error'):
        return False
    if not self.scope['user'] or self.scope['user'] is AnonymousUser:
        return False
    return True


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        # Check if user is authenticated
        if self.is_error_exists():
            error = {
                'error': str(self.scope['error'])
            }
            self.send(text_data=json.dumps(error))
            self.close()

        else:            
            # Check if user is a participant of the conversation
            if Conversation.objects.filter(id=int(self.room_name), participants=self.scope['user']).exists():
                async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name)
            else:
                self.send(text_data=json.dumps({'error': 'You are not a participant of this conversation'}))
                self.close(code=4003)
        


    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        if self.scope.get('user') is not None:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )

    def chat_message(self, event):
        text_data_json = event.copy()
        text_data_json.pop('type')
        message, attachment = (text_data_json['message'], text_data_json.get('attachment', None))

        conversation = Conversation.objects.get(id=int(self.room_name))
        sender = self.scope['user']

        if attachment:
            file_str, file_ext = attachment['data'], attachment['format']
            file_data = ContentFile(base64.b64decode(file_str), name=f'{secrets.token_hex(8)}.{file_ext}')
            _message = Message.objects.create(conversation=conversation, sender=sender, attachment=file_data, text=message)
        else:
            _message = Message.objects.create(conversation=conversation, sender=sender, content=message)
        
        serializer = MessageSerializer(instance=_message)
        
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': serializer.data
        }))

    def is_error_exists(self):
        """This checks if error exists during websockets"""

        return True if 'error' in self.scope else False
