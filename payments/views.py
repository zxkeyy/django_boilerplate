from django.conf import settings
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
import stripe

class StripeConfigView(viewsets.ViewSet):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return Response(stripe_config)

# Create your views here.
class CreateCheckoutSessionView(APIView):
    def post(self, request, *args, **kwargs):
        line_items = request.data['line_items']
        try:
            domain_url = "http://localhost:8000" # Change to Fromtend URL
            stripe.api_key = settings.STRIPE_SECRET_KEY
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + '/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + '/cancel/',
                payment_method_types=['card'],
                mode='payment',
                line_items=line_items
            )
            return Response({'sessionId': checkout_session['id']})
        except Exception as e:
            return Response({'error': str(e)})