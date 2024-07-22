from django.urls import path
from .views import CreateCheckoutSessionView, StripeConfigView, StripeWebhookView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('stripe/config', StripeConfigView, basename='stripe-config')
router.register('stripe/create-checkout-session', CreateCheckoutSessionView, basename='stripe-create-checkout-session')
router.register('stripe/webhook', StripeWebhookView, basename='stripe-webhook')

urlpatterns = router.urls

# urlpatterns2 = [
#     path('stripe/config', StripeConfigView.as_view({'get': 'get'}), name='stripe-config'),
#     path('stripe/create-checkout-session', CreateCheckoutSessionView.as_view({'post': 'create'}), name='stripe-create-checkout-session'),
# ]