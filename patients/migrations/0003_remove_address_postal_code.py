# Generated by Django 2.0 on 2019-06-22 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0002_address_district'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='postal_code',
        ),
    ]