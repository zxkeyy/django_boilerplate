# Generated by Django 5.0.6 on 2024-07-22 17:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ecommerce', '0005_alter_order_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StripePayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_charge_id', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stripe_payments', to='ecommerce.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stripe_payments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
