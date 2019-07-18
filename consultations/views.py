from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect

from django.shortcuts import render, redirect

from datetime import datetime, timedelta

# forms
from consultations.Forms.ConsultationForm import ConsultationForm
from consultations.Forms.EventForm import EventForm
from consultations.Forms.ProcedureForm import ProcedureForm
from financier.forms import PatientFinancialForm
# models
from consultations.models import Consultation
from consultations.models import Event
from consultations.models import Procedure
from financier.models import Plots
from financier.models import PatientFinancial


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
        if request.method == "POST" and form.is_valid() and form_payment.is_valid():
            consultation = form.save()
            patient_financier = form_payment.save()
            plots_price = (patient_financier.amount-patient_financier.amount_paid)/patient_financier.num_plots

            #plots = Plots.create(patient_financier.amount, patient_financier.num_plots, patient_financier.payday)
            if patient_financier.amount_paid > 0:
                plots = Plots()
                plots.create(patient_financier.amount_paid, datetime.now(), patient_financier, 1, True)
                plots.pay(datetime.now())

            for i in range(0, patient_financier.num_plots):
                plots = Plots()
                date = patient_financier.payday + timedelta(days=(30*(i+1)))
                plots.create(plots_price, date, patient_financier)

            patient_financier.consultation = consultation
            patient_financier.save()
            messages.add_message(request, messages.SUCCESS, 'Consulta Agendada!')
            return redirect('schedule')
    else:
        form = EventForm(request.POST or None, request.FILES or None)
        if request.method == "POST" and form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Evento Agendado!')
            return redirect('schedule')
    if type == 'consultation':
        return render(request, 'schedule/new.html', {'form': form, 'form_payment': form_payment, 'type': type})
    return render(request, 'schedule/new.html', {'form': form, 'type': type})


@login_required
def edit(request, type, id):
    if type == 'consultation':
        consultation = Consultation.objects.get(pk=id)
        form = ConsultationForm(request.POST or None, request.FILES or None, instance=consultation)
        if request.method == "POST" and form.is_valid():
            form.save()
            return redirect('schedule')
    else:
        event = Event.objects.get(pk=id)
        form = EventForm(request.POST or None, request.FILES or None, instance=event)
    return render(request, 'schedule/edit.html', {'form': form, 'type': type})


@login_required
def view(request, id):
    consultation = Consultation.objects.get(pk=id)
    patient_financier = PatientFinancial.objects.filter(consultation=consultation)
    patient_financier = patient_financier[0]
    plots = Plots.objects.filter(patient_financial=patient_financier)
    return render(request, 'schedule/view.html', {'consultation': consultation, 'patient_financier': patient_financier, 'plots': plots})


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
    consultation = Consultation.objects.get(pk=id)
    if consultation.delete():
        messages.add_message(request, messages.SUCCESS, 'Consulta Cancelada/Excluida!')
    if location == "patient":
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
    return redirect('schedule')

def delete_procedure(request, id):
    procedure = Procedure.objects.get(pk=id)
    if procedure.delete():
        messages.add_message(request, messages.SUCCESS, 'Procedimento Excluido!')
    return redirect('procedures')

def delete_schedule(request, id):
    schedule = Consultation.objects.get(pk=id)
    if schedule.delete():
        messages.add_message(request, messages.SUCCESS, 'Consulta Cancelada/Excluida!')
    return redirect('schedule')