from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
import stripe
from chargily_pay import ChargilyClient
from chargily_pay.entity import Checkout

from django_boilerplate.settings import AUTH_USER_MODEL
from ecommerce.models import Order, Product
from ecommerce.serializers import OrderSerializer
from .models import StripePayment
from .serializers import CreateCheckoutSessionSerializer, StripePaymentSerializer

class StripePaymentViewSet(viewsets.ModelViewSet):
    queryset = StripePayment.objects.all()
    serializer_class = StripePaymentSerializer
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ['get']

class StripeConfigView(viewsets.ViewSet):
    permission_classes = []

    def list(self, request):
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return Response(stripe_config)


class CreateStripeCheckoutSessionView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateCheckoutSessionSerializer

    def list(self, request):
        return Response({'error': 'Please provide an order id in the request body.'}, status=400)

    def create(self, request):
        order_id = request.data.get('order_id')
        success_url = request.data.get('success_url')
        cancel_url = request.data.get('cancel_url')
        if not order_id:
            return Response({'error': 'Please provide an order id in the request body.'}, status=400)
        line_items = []
        order = Order.objects.get(id=order_id)
        if order.status != 'checkout':
            return Response({'error': 'This order has already been paid for or canceled.'}, status=400)
        for item in order.items.all():
            try:
                product = item.product
                line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': product.name,
                            'images': [settings.BASE_URL + product.images.first().image.url],
                        },
                        'unit_amount': int(item.price * 100),
                    },
                    'quantity': item.quantity,
                })
            except Product.DoesNotExist:
                return Response({'error': 'One of the products in the order does not exist. id = ' + item.product}, status=400)
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            checkout_session = stripe.checkout.Session.create(
                success_url=success_url+'?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=cancel_url,
                payment_method_types=['card'],
                mode='payment',
                metadata={'order_id': order.id, 'user_id': request.user.id},
                line_items=line_items
            )
            return Response({'checkout_url': checkout_session['url']})
        except Exception as e:
            return Response({'error': str(e)})
        
class StripeWebhookView(viewsets.ViewSet):
    permission_classes = []
    
    @csrf_exempt
    def create(self, request):
        endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            return Response(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return Response(status=400)

        # Handle the event
        if event['type'] == 'checkout.session.completed':
            try:
                session = event['data']['object']
                user = session['metadata']['user_id']
                order_id = session['metadata']['order_id']
                stripePayment = StripePayment.objects.create(
                    user= get_user_model().objects.get(id=user),
                    stripe_charge_id=session['payment_intent'],
                    amount=session['amount_total'] / 100,
                    order_id=order_id
                )
                stripePayment.save()
                order = Order.objects.get(id=order_id)
                order.status = 'pending'
                order.save()
            except Exception as e:
                print(str(e))
                return Response(status=400)
        return Response(status=200)
    
client = ChargilyClient(
                secret=settings.CHARGILY_SECRET,
                key=settings.CHARGILY_KEY,
                url=settings.CHARGILY_URL
            )
    
class CreateChargilyCheckoutSessionView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateCheckoutSessionSerializer

    def list(self, request):
        return Response({'error': 'Please provide an order id in the request body.'}, status=400)

    def create(self, request):
        order_id = request.data.get('order_id')
        success_url = request.data.get('success_url')
        cancel_url = request.data.get('cancel_url')
        if not order_id:
            return Response({'error': 'Please provide an order id in the request body.'}, status=400)
        order = Order.objects.get(id=order_id)
        if order.status != 'checkout':
            return Response({'error': 'This order has already been paid for or canceled.'}, status=400)
        try:
            checkout = Checkout(
                amount=int(order.total),
                currency='dzd',
                success_url=success_url,
                failure_url=cancel_url,
                #webhook_endpoint= '',
                metadata={'order_id': order.id, 'user_id': request.user.id}
            )
            checkout_session = client.create_checkout(checkout)
            return Response({'checkout_url': checkout_session['checkout_url']})
        except Exception as e:
            return Response({'error': str(e)})
        
class ChargilyWebhookView(viewsets.ViewSet):
    permission_classes = []

    @csrf_exempt
    def create(self, request):
        return Response(status=200)