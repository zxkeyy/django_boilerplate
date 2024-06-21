from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from profiles.filters import ProfileFilter
from profiles.models import Profile
from profiles.permissions import IsOwnerOrReadOnly
from profiles.serializers import ProfileSerializer

# Create your views here.
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly|permissions.IsAdminUser]
    lookup_field = 'user__username'

    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = ProfileFilter
    search_fields = ['user__username']