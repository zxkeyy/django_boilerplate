from django.urls import path
from .views import StripeConfigView
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('stripe/config', StripeConfigView.as_view({'get': 'get'}), name='stripe-config'),
]