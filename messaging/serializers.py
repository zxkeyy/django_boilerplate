from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Conversation, ConversationParticipant, Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'attachment', 'is_deleted', 'created_at', 'updated_at']

class ConversationParticipantSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    
    class Meta:
        model = ConversationParticipant
        fields = ['id', 'username', 'is_admin']

class ConversationListSerializer(serializers.ModelSerializer):
    participants = ConversationParticipantSerializer(many=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'name', 'participants', 'last_message', 'created_at', 'updated_at']

    def get_last_message(self, obj):
        last_message = obj.messages.first()
        if last_message:
            return MessageSerializer(last_message).data
        return None
    
class ConversationSerializer(serializers.ModelSerializer):
    participants = ConversationParticipantSerializer(source='participant_set' ,many=True)
    messages = MessageSerializer(many=True)

    class Meta:
        model = Conversation
        fields = ['id', 'name', 'participants', 'messages', 'created_at', 'updated_at']

class AddParticipantSerializer(serializers.Serializer):
    username = serializers.CharField()
    is_admin = serializers.BooleanField(default=False)

class ToggleAdminSerializer(serializers.Serializer):
    username = serializers.CharField()

class RemoveParticipantSerializer(serializers.Serializer):
    username = serializers.CharField()