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
    startTime = models.TimeField(blank=True,null=True)
    end = models.DateField(blank=True, null=True)
    endTime = models.TimeField(blank=True, null=True)
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
        item = {'id': self.id, 'title': self.title,
                'redirect_url': reverse('edit_schedules', kwargs={'type': 'event', 'id': self.id}),
                'background_color': self.backgroundColor, 'textColor': self.textColor, 'borderColor': '#ffffff',
                'type': 'event', 'allDay': self.allDay, 'rendering': self.get_rendering()}
        print(item)
        if self.allDay:
            item['start'] =  self.start
            if self.end:
                item['end'] =  self.end
        else:
            if self.startTime:
                item['start'] = get_full_date(self.start, self.startTime)
                if self.end:
                    if self.endTime:
                        item['end'] = get_full_date(self.end, self.endTime)
                    else:
                        if self.startTime:
                            item['end'] = get_full_date(self.end, self.startTime)
                        else:
                            item['end'] =  self.end
            else:
                item['start'] = self.start
                if self.end:
                    item['end'] =  self.end
        return item