from django.urls import path
from profiles.views import ProfileViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router .register('', ProfileViewSet)

urlpatterns = router.urls