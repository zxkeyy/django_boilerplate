from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import IsConversationAdminOrReadOnly
from .serializers import AddParticipantSerializer, ConversationListSerializer, ConversationParticipantSerializer, ConversationSerializer, MessageSerializer, RemoveParticipantSerializer, ToggleAdminSerializer
from .models import Conversation, ConversationParticipant, Message

# Create your views here.
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsConversationAdminOrReadOnly]

    def get_queryset(self):
        return self.request.user.conversations.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ConversationListSerializer
        return super().get_serializer_class()
    
    def perform_create(self, serializer):
        conversation = serializer.save()
        ConversationParticipant.objects.create(conversation=conversation, user=self.request.user, is_admin=True)

    @action(detail=True, methods=['post'], serializer_class=AddParticipantSerializer, permission_classes=[permissions.IsAuthenticated, IsConversationAdminOrReadOnly])
    def add_participant(self, request, pk=None):
        conversation = self.get_object()
        user = get_user_model().objects.get(username=request.data['username'])
        is_admin = request.data.get('is_admin', False)
        ConversationParticipant.objects.create(conversation=conversation, user=user, is_admin=is_admin)
        return Response({'status': 'participant added'})

    @action(detail=True, methods=['post'], serializer_class=RemoveParticipantSerializer, permission_classes=[permissions.IsAuthenticated, IsConversationAdminOrReadOnly])
    def remove_participant(self, request, pk=None):
        conversation = self.get_object()
        user = get_user_model().objects.get(username=request.data['username'])
        ConversationParticipant.objects.filter(conversation=conversation, user=user).delete()
        return Response({'status': 'participant removed'})

    @action(detail=True, methods=['post'], serializer_class=ToggleAdminSerializer, permission_classes=[permissions.IsAuthenticated, IsConversationAdminOrReadOnly])
    def toggle_admin(self, request, pk=None):
        conversation = self.get_object()
        user = get_user_model().objects.get(username=request.data['username'])
        participant = ConversationParticipant.objects.get(conversation=conversation, user=user)
        participant.is_admin = not participant.is_admin
        participant.save()
        return Response({'status': 'admin status toggled'})

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.messages.all()

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)