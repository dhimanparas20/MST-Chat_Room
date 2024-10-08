# Generated by Django 5.0.7 on 2024-08-05 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_rename_userdetails_userdetail'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='groupmessage',
            options={'ordering': ('-timestamp',)},
        ),
        migrations.AddField(
            model_name='groupmessage',
            name='sender_username',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='groupKey',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
