from django.conf import settings
from django.db import models

# Create your models here.
class StripePayment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='stripe_payments')
    stripe_charge_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey('ecommerce.Order', on_delete=models.PROTECT, related_name='stripe_payments')
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.stripe_charge_id
    
class ChargilyPayment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='chargily_payments')
    chargily_charge_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey('ecommerce.Order', on_delete=models.PROTECT, related_name='chargily_payments')

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.chargily_charge_id