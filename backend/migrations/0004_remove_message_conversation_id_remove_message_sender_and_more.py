# Generated by Django 5.0.7 on 2024-08-05 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_alter_groupmessage_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='conversation_id',
        ),
        migrations.RemoveField(
            model_name='message',
            name='sender',
        ),
        migrations.DeleteModel(
            name='Conversation',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]
