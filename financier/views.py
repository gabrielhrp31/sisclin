from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.serializers import json
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from .models import PatientFinancial
from .models import Plots
from .forms import PatientFinancialForm
from patients.Forms.PatientForm import PatientForm
from consultations.Forms.ConsultationForm import ConsultationForm


def index(request):
    return render(request, 'financier.html')


@login_required
def list_patients_financier(request):
    patients_financier = PatientFinancial.objects.all()
    if request.method == "GET" and request.is_ajax():
        data = []
        for financier in patients_financier:
            data.append(financier.as_dict())
        return JsonResponse(data, safe=False)
    return render(request, 'accounting/list.html', {'patients_financier': patients_financier})


@login_required
def new_patient_financier(request):
    patient_financier_form = PatientFinancialForm(request.POST or None, request.FILES or None)
    patient_form = PatientForm(request.POST or None, request.FILES or None)
    consultation_form = ConsultationForm(request.POST or None, request.FILES or None)
    print('Fora')
    if request.method == "POST":
        # print('PATIENT')
        # print(patient_form.errors)
        # print('CONSULTATION')
        # print(consultation_form.errors)
        if patient_financier_form.is_valid() and patient_form.is_valid() and consultation_form.is_valid():
            print('TOP')
            patient_financier = patient_financier_form.save()
            patient = patient_form.save()
            consultation = consultation_form.save()

            #plots = Plots(patient_financier.amount, patient_financier.num_plots, patient_financier.payday)

            patient_financier.patient_id = patient.id
            patient_financier.consultation_id = consultation.id
            
            patient_financier.save()
            messages.add_message(request, messages.SUCCESS, 'Lançamento Cadastrado')
            return redirect('list_patients_financier')
    return render(request, 'accounting/new.html', {'patient_financier_form': patient_financier_form})

def get_status_display(request):
    pass