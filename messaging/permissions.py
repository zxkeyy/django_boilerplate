from rest_framework import permissions
from .models import ConversationParticipant

class IsConversationAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Check if the user is an admin of the conversation
        participant = ConversationParticipant.objects.get(conversation=obj, user=request.user)
        return participant.is_admin
    
class IsConversationParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant of the conversation
        return ConversationParticipant.objects.filter(conversation=obj, user=request.user).exists()