# Generated by Django 5.0.6 on 2024-06-23 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0002_alter_conversationparticipant_conversation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='attachments'),
        ),
    ]