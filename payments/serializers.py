from rest_framework import serializers

from payments.models import StripePayment

class CreateCheckoutSessionSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    class Meta:
        fields = ['order_id']

class StripePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StripePayment
        fields = ['id', 'user', 'stripe_charge_id', 'amount', 'order', 'timestamp']
        read_only_fields = ['stripe_charge_id', 'timestamp']
