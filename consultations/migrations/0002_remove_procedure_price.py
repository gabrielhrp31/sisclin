# Generated by Django 2.0 on 2019-07-19 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='procedure',
            name='price',
        ),
    ]
