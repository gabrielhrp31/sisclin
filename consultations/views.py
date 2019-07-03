from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from consultations.Forms.ConsultationForm import ConsultationForm
from consultations.Forms.EventForm import EventForm
from consultations.models import Consultation
from consultations.models import Event


@login_required
def index(request):
    return render(request, 'schedule/index.html')


@login_required
def get_schedules(request):
    consultations = Consultation.objects.all()
    events = Event.objects.all()
    data = []
    for consultation in consultations:
        data.append(consultation.as_dict())
    for event in events:
        data.append(event.as_dict())
    return JsonResponse(data, safe=False)


@login_required
def new_schedule(request, type):
    if type == 'consultation':
        form = ConsultationForm(request.POST or None, request.FILES or None)
    else:
        form = EventForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        # messages.add_message(request, messages.success, 'Agendamento Concluido')
        return redirect('schedule')
    return render(request, 'schedule/new_schedule.html', {'form': form, 'type': type})


def view_edit(request,type, id):
    if type == 'consultation':
        consultation = Consultation.objects.get(pk=id)
        form = ConsultationForm(request.POST or None, request.FILES or None, instance=consultation)
    else:
        event = Event.objects.get(pk=id)
        form = EventForm(request.POST or None, request.FILES or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('schedule')
    return render(request, 'schedule/view_edit.html', {'form': form, 'type': type})
