from django.db import models

from patients.Models.Patient import Patient


class Consultation(models.Model):
    allDay = models.BooleanField(default=False)
    start = models.DateTimeField(null=False)
    end = models.DateTimeField(null=False)
    title = models.TextField(null=False)
    backgroundColor = models.CharField(max_length=7)
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def as_dict(self):
        return {
            'id': self.id,
            'allDay': self.allDay,
            'start': self.start.date(),
            'startTime': self.start.time(),
            'end': self.end.date(),
            'endTime': self.end.time(),
            'title': self.title,
            'backgroundColor': self.backgroundColor,
            'patient': self.patient.id
        }
