from rest_framework import serializers

from payments.models import ChargilyPayment, StripePayment

class CreateCheckoutSessionSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    success_url = serializers.CharField()
    cancel_url = serializers.CharField()
    class Meta:
        fields = ['order_id', 'success_url', 'cancel_url']

class StripePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StripePayment
        fields = ['id', 'user', 'stripe_charge_id', 'amount', 'order', 'timestamp']
        read_only_fields = ['stripe_charge_id', 'timestamp']

class ChargilyPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargilyPayment
        fields = ['id', 'user', 'chargily_charge_id', 'amount', 'order', 'timestamp']
        read_only_fields = ['chargily_charge_id', 'timestamp']
