from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.StripePayment)
class StripePaymentAdmin(admin.ModelAdmin):
    list_display = ['id' ,'user', 'stripe_charge_id', 'amount', 'order', 'timestamp']
    search_fields = ['user__username', 'stripe_charge_id', 'order__id']
    list_filter = ['timestamp']
    list_editable = ['amount']
    readonly_fields = ['stripe_charge_id', 'timestamp']
    class Meta:
        model = models.StripePayment

@admin.register(models.ChargilyPayment)
class ChargilyPaymentAdmin(admin.ModelAdmin):
    list_display = ['id' ,'user', 'chargily_charge_id', 'amount', 'order', 'timestamp']
    search_fields = ['user__username', 'chargily_charge_id', 'order__id']
    list_filter = ['timestamp']
    list_editable = ['amount']
    readonly_fields = ['chargily_charge_id', 'timestamp']
    class Meta:
        model = models.ChargilyPayment