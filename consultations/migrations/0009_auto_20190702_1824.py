# Generated by Django 2.0 on 2019-07-02 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0008_auto_20190702_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultation',
            name='patient',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='patients.Patient'),
        ),
    ]