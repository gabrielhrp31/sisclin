from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from consultations.models import Consultation


@login_required
def index(request):
    return render(request, 'schedule.html')


@login_required
def get_consultations(request):
    consultations = Consultation.objects.all()
    data = []
    for consultation in consultations:
        data.append(consultation.as_dict())
    print(JsonResponse(data, safe=False).serialize())
    return JsonResponse(data, safe=False)

