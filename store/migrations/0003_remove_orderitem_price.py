# Generated by Django 5.1.6 on 2025-02-24 03:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='price',
        ),
    ]
