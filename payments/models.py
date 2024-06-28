from django.conf import settings
from django.db import models

# Create your models here.
class StripePayment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stripe_payments')
    stripe_charge_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.stripe_charge_id