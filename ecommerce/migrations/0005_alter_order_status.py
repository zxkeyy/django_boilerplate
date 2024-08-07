# Generated by Django 5.0.6 on 2024-07-22 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0004_remove_order_payment_alter_order_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('checkout', 'Checkout'), ('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='checkout', max_length=100),
        ),
    ]
