from django.contrib import admin
from consultations.models import Consultation
from consultations.models import Event


# Register your models here.
admin.site.register(Consultation)
admin.site.register(Event)
