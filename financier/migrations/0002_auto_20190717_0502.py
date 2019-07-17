# Generated by Django 2.0 on 2019-07-17 08:02

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0003_remove_consultation_title'),
        ('financier', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost_type', models.NullBooleanField()),
                ('description', models.TextField(null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=7)),
                ('payment_form', models.NullBooleanField()),
                ('num_plots', models.IntegerField(null=True)),
                ('payday', models.DateField(null=True)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('change_date', models.DateField(auto_now=True)),
                ('change_hour', models.TimeField(auto_now=True)),
                ('status', models.NullBooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Plots',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('date', models.DateField(null=True)),
                ('paid_day', models.DateField(null=True)),
                ('input', models.BooleanField(default=False)),
                ('type', models.IntegerField(default=2)),
                ('cost', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='financier.Cost')),
            ],
        ),
        migrations.RemoveField(
            model_name='patientfinancial',
            name='consultation_id',
        ),
        migrations.RemoveField(
            model_name='patientfinancial',
            name='outstanding_balance',
        ),
        migrations.RemoveField(
            model_name='patientfinancial',
            name='patient_id',
        ),
        migrations.RemoveField(
            model_name='patientfinancial',
            name='plots',
        ),
        migrations.RemoveField(
            model_name='patientfinancial',
            name='status',
        ),
        migrations.AddField(
            model_name='patientfinancial',
            name='consultation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='consultations.Consultation', verbose_name='Consulta'),
        ),
        migrations.AddField(
            model_name='patientfinancial',
            name='num_plots',
            field=models.IntegerField(default='1'),
        ),
        migrations.AlterField(
            model_name='patientfinancial',
            name='payday',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='plots',
            name='patient_financial',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='financier.PatientFinancial'),
        ),
    ]