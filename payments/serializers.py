from rest_framework import serializers

from payments.models import StripePayment

class CreateCheckoutSessionSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    class Meta:
        fields = ['order_id']
