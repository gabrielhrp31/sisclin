from datetime import datetime

from django.db import models
from django.urls import reverse

from patients.Models.Patient import Patient


def get_full_date(date, time):
    str = date.strftime("%d/%m/%Y")+" "+time.strftime("%H:%M:%S")
    full_date = datetime.strptime(str, "%d/%m/%Y %H:%M:%S")
    return full_date


class Consultation(models.Model):
    title = models.TextField(null=False)
    date = models.DateField(null=False)
    startTime = models.TimeField(null=False, default=datetime.now())
    endTime = models.TimeField(null=False, default=datetime.now())
    description = models.TextField(null=True, blank=True)
    payment = models.BooleanField(null=False, default=False)
    backgroundColor = models.CharField(max_length=7, default="#000000")
    textColor = models.CharField(max_length=7, default="#ffffff")
    patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def as_dict(self):
        return {
            'id': self.id,
            'allDay': False,
            'start': get_full_date(self.date, self.startTime),
            'end': get_full_date(self.date, self.endTime),
            'title': self.title,
            'url': reverse('view_edit_schedules', kwargs={'type': 'consultation', 'id': self.id}),
            'backgroundColor': self.backgroundColor,
            'textColor': self.textColor,
            'patient': self.patient.id,
            'type': 'consultation',
            'borderColor': '#ffffff',
        }
