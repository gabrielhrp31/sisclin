# Generated by Django 2.0 on 2019-07-11 05:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('financier', '0004_plots'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientfinancial',
            name='num_plots',
            field=models.IntegerField(default='1'),
        ),
        migrations.AlterField(
            model_name='patientfinancial',
            name='plots',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='financier.Plots'),
        ),
    ]
