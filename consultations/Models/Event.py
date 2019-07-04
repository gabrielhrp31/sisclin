from datetime import datetime

from django.db import models
from django.urls import reverse

from patients.Models.Patient import Patient


def get_full_date(date, time):
    str = date.strftime("%d/%m/%Y")+" "+time.strftime("%H:%M:%S")
    full_date = datetime.strptime(str, "%d/%m/%Y %H:%M:%S")
    return full_date


class Event(models.Model):
    title = models.TextField(null=False)
    start = models.DateField(null=False)
    startTime = models.TimeField(null=True)
    end = models.DateField(null=False)
    endTime = models.TimeField(null=True)
    description = models.TextField(null=True)
    allDay = models.BooleanField(default=False)
    holiday = models.BooleanField(default=False)
    backgroundColor = models.CharField(max_length=7, default="#000000")
    textColor = models.CharField(max_length=7, default="#ffffff")

    def __str__(self):
        return self.title

    def get_rendering(self):
        if self.holiday:
            return 'background'
        else:
            return ''

    def as_dict(self):
        return {
            'id': self.id,
            'allDay': self.allDay,
            'start': get_full_date(self.start, self.startTime),
            'end': get_full_date(self.end, self.endTime),
            'title': self.title,
            'url': reverse('view_edit_schedules',  kwargs={'type': 'event', 'id': self.id}),
            'backgroundColor': self.backgroundColor,
            'textColor': self.textColor,
            'borderColor': '#ffffff',
            'type': 'event',
            'rendering': self.get_rendering()
        }
