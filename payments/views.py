from django.conf import settings
from django.http import JsonResponse
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
import stripe

from ecommerce.models import Order, Product
from ecommerce.serializers import OrderSerializer
from payments.serializers import CreateCheckoutSessionSerializer

class StripeConfigView(viewsets.ViewSet):
    permission_classes = []

    def list(self, request):
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return Response(stripe_config)

# Create your views here.
class CreateCheckoutSessionView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateCheckoutSessionSerializer

    def list(self, request):
        return Response({'error': 'Please provide an order id in the request body.'}, status=400)

    def create(self, request):
        order_id = request.data.get('order_id')
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
            domain_url = "http://localhost:8000" # Change to Frontend URL
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