# Generated by Django 2.2.3 on 2019-07-11 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financier', '0007_auto_20190711_0539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plots',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
