from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Conversation, ConversationParticipant, Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id','conversation', 'sender', 'content', 'attachment', 'is_deleted', 'created_at', 'updated_at']

class ConversationParticipantSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    
    class Meta:
        model = ConversationParticipant
        fields = ['id', 'username', 'is_admin']

class ConversationListSerializer(serializers.ModelSerializer):
    participant_set = ConversationParticipantSerializer(many=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'name', 'participant_set', 'last_message', 'created_at', 'updated_at']

    def get_last_message(self, obj):
        last_message = obj.messages.first()
        if last_message:
            return MessageSerializer(last_message).data
        return None
    
class ConversationSerializer(serializers.ModelSerializer):
    participants = ConversationParticipantSerializer(source='participant_set' ,many=True)
    last_50_messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'name', 'participants', 'last_50_messages', 'created_at', 'updated_at']

    def get_last_50_messages(self, obj):
        messages = obj.messages.all().order_by('-created_at')[:50]
        if messages:
            return MessageSerializer(messages, many=True).data
        return None

class AddParticipantSerializer(serializers.Serializer):
    username = serializers.CharField()
    is_admin = serializers.BooleanField(default=False)

class ToggleAdminSerializer(serializers.Serializer):
    username = serializers.CharField()

class RemoveParticipantSerializer(serializers.Serializer):
    username = serializers.CharField()