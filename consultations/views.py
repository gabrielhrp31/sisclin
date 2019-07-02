from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from consultations.Forms.ConsultationForm import ConsultationForm
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
    return JsonResponse(data, safe=False)


@login_required
def new_consultation(request):
    consultation_form = ConsultationForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and consultation_form.is_valid():
        consultation_form.save()
        # messages.add_message(request, messages.success, 'Agendamento Concluido')
        return redirect('schedule')
    return render(request, 'new_schedule.html', {'consultation_form': consultation_form})
