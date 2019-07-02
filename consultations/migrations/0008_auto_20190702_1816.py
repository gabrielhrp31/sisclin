# Generated by Django 2.0 on 2019-07-02 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0007_consultation_holiday'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultation',
            name='endTime',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='consultation',
            name='startTime',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='consultation',
            name='end',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='consultation',
            name='start',
            field=models.DateField(),
        ),
    ]