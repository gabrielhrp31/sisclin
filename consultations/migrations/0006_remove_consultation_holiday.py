# Generated by Django 2.0 on 2019-07-02 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0005_auto_20190702_1726'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consultation',
            name='holiday',
        ),
    ]