from django_filters.rest_framework import FilterSet
from profiles.models import Profile

class ProfileFilter(FilterSet):
    class Meta:
        model = Profile
        fields = []