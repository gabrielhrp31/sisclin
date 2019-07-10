from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect

from django.shortcuts import render, redirect

# forms
from consultations.Forms.ConsultationForm import ConsultationForm
from consultations.Forms.EventForm import EventForm
from consultations.Forms.ProcedureForm import ProcedureForm
from financier.forms import PatientFinancialForm
# models
from consultations.models import Consultation
from consultations.models import Event
from consultations.models import Procedure


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
    form_payment = None
    if type == 'consultation':
        form = ConsultationForm(request.POST or None, request.FILES or None)
        form_payment = PatientFinancialForm(request.POST or None, request.FILES or None)
        print(form_payment.errors)
        if request.method == "POST" and form.is_valid() and form_payment.is_valid():
            consultation = form.save()
            patient_financial = form_payment.save()
            patient_financial.consultation = consultation
            patient_financial.save()
            # messages.add_message(request, messages.success, 'Agendamento Concluido')
            return redirect('schedule')
    else:
        form = EventForm(request.POST or None, request.FILES or None)
        if request.method == "POST" and form.is_valid():
            form.save()
            # messages.add_message(request, messages.success, 'Agendamento Concluido')
            return redirect('schedule')
    if type == 'consultation':
        return render(request, 'schedule/new.html', {'form': form, 'form_payment': form_payment, 'type': type})
    return render(request, 'schedule/new.html', {'form': form, 'type': type})


@login_required
def view_edit(request, type, id):
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


@login_required
def list_procedures(request):
    procedures = Procedure.objects.all()
    if request.is_ajax():
        data = []
        for procedure in procedures:
            data.append(procedure.as_dict())
        return JsonResponse(data, safe=False)
    return render(request, 'procedures/list.html', {'procedures': procedures})


@login_required
def new_procedure(request):
    form = ProcedureForm(request.POST or None, request.FILES or None)
    if form.is_valid() and request.method == 'POST':
        form.save()
        messages.add_message(request, messages.SUCCESS, 'Procedimento Cadastrado')
        return redirect('procedures')
    return render(request, 'procedures/new.html', {'form': form})


@login_required
def view_edit_procedure(request, id):
    procedure = Procedure.objects.get(pk=id)
    if request.is_ajax() and request.method == "GET":
        return JsonResponse(procedure.as_dict(), safe=False)
    else:
        form = ProcedureForm(request.POST or None, request.FILES or None, instance=procedure)
        if form.is_valid and request.method == 'POST':
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Procedimento Editado')
            return redirect('procedures')
    return render(request, 'procedures/view_edit.html', {'form': form})


def delete_consultation(request, id, location):
    procedure = Consultation.objects.get(pk=id)
    if procedure.delete():
        messages.add_message(request, messages.SUCCESS, 'Consulta Cancelada/Excluida!')
    if location == "patient":
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
    return redirect('schedule')
