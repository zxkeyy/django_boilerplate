from django.urls import path
from .views import ChargilyPaymentViewSet, ChargilyWebhookView, CreateStripeCheckoutSessionView, StripeConfigView, StripeWebhookView, StripePaymentViewSet, CreateChargilyCheckoutSessionView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('stripe/payments', StripePaymentViewSet)
router.register('stripe/create-checkout-session', CreateStripeCheckoutSessionView, basename='stripe-create-checkout-session')
router.register('stripe/webhook', StripeWebhookView, basename='stripe-webhook')
router.register('stripe/config', StripeConfigView, basename='stripe-config')
router.register('chargily/payments', ChargilyPaymentViewSet)
router.register('chargily/create-checkout-session', CreateChargilyCheckoutSessionView, basename='chargily-create-checkout-session')
router.register('chargily/webhook', ChargilyWebhookView, basename='chargily-webhook')

urlpatterns = router.urls