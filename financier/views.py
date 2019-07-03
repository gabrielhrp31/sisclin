from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.serializers import json
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from .models import PatientFinancial
from .forms import PatientFinancialForm


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
    if request.method == "POST":
        if patient_financier_form.is_valid():
            patient_financier_form.save()
            messages.add_message(request, messages.SUCCESS, 'Lançamento Cadastrado')
            return redirect('list_patients_financier')
    return render(request, 'accounting/new.html', {'patient_financier_form': patient_financier_form})