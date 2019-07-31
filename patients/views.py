from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.serializers import json
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from datetime import date
from collections import OrderedDict


# Create your views here.
from .models import Address
from .models import Patient
from consultations.models import Consultation
from .forms import AddressForm
from .forms import PatientForm


@login_required
def list_patients(request):
    patients = Patient.objects.all()
    return render(request, 'patients/list.html', {'patients': patients})


@login_required
def get_patients(request):
    patients = Patient.objects.all()
    data = []
    for patient in patients:
        data.append(patient.as_dict())
    return JsonResponse(data, safe=False)


@login_required
def new_patient(request):
    patient_form = PatientForm(request.POST or None, request.FILES or None)
    address_form = AddressForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if patient_form.is_valid():
            patient_form.save()
            messages.add_message(request, messages.SUCCESS, 'Paciente Cadastrado')
            return redirect('list_patients')
    return render(request, 'patients/new.html', {'patient_form': patient_form, 'address_form':address_form})


@login_required
def edit_patient(request, id):
    patient = Patient.objects.get(pk=id)
    address = Address.objects.get(pk=patient.address.id)
    patient_form = PatientForm(request.POST or None, request.FILES or None, instance=patient)
    address_form = AddressForm(request.POST or None, request.FILES or None, instance=address)
    if request.method == "POST":
        if patient_form.is_valid():
            patient_form.save()
            messages.add_message(request, messages.SUCCESS, 'Paciente Editado')
            return redirect('list_patients')
    return render(request, 'patients/edit.html', {'patient_form': patient_form, 'address_form': address_form, 'address': address})


@login_required
def view_patient(request, id):
    patient = Patient.objects.get(pk=id)
    consultations = Consultation.objects.filter(patient=id)
    consultations_timeline = {}
    for consultation in consultations:
        if not (consultation.date in consultations_timeline.keys()):
            consultations_timeline[consultation.date] = []
            consultations_timeline[consultation.date].append(consultation)
        else:
            consultations_timeline[consultation.date].append(consultation)
    consultations_timeline = OrderedDict(sorted(consultations_timeline.items(), key=lambda t: t[0], reverse=True))
    return render(request, 'patients/view.html', {'patient': patient, 'consultations': consultations_timeline, 'today': date.today()})


@login_required
def get_patient(request, id):
    patient = Patient.objects.get(pk=id)
    data = patient.as_dict()
    return JsonResponse(data, safe=False)


@login_required
def list_address(request):
    addresses = Address.objects.all()
    return render(request, 'address/list.html', {'addresses': addresses})


@login_required
def get_address(request):
    addresses = Address.objects.all()
    data = []
    for address in addresses:
        data.append(address.as_dict())
    return JsonResponse(data, safe=False)


@login_required
def list_address(request):
    addresses = Address.objects.all()
    return render(request, 'address/list.html', {'addresses': addresses})


@login_required
def new_address(request):
    form = AddressForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and request.is_ajax():
        address = Address(number=request.POST['number'], city=request.POST['city'], country=request.POST['country'], district=request.POST['district'], street=request.POST['street'])
        if address.is_valid():
            address.save()
            data = dict({'success': True, 'message': 'Endereço Criado com Sucesso', 'id': address.id})
        else:
            data = dict({'success': False, 'title': 'Campos Invalidos!', 'message': 'Erro ao criar endereço todos os campos devem ser alfa numericos e não podem estar vazios'})
        return JsonResponse(data)
    elif request.method == "POST" and not request.is_ajax():
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Endereço cadastrado')
            return redirect('get_address')
    return render(request, 'address/new.html', {'form': form})

@login_required
def view_edit_address(request, id):
    address = Address.objects.get(pk=id)
    form = AddressForm(request.POST or None, request.FILES or None, instance=address)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Endereço Editado')
            return redirect('get_address')
    return render(request, 'address/view_edit.html', {'form': form})

@login_required
def delete_address(request, id):
    address = Address.objects.get(pk=id)
    if address.delete():
        messages.add_message(request, messages.SUCCESS, 'Endereço Deletado')
    return redirect('get_address')

@login_required
def delete_patient(request, id):
    patient = Patient.objects.get(pk=id)
    if patient.delete():
        messages.add_message(request, messages.SUCCESS, 'Paciente Deletado!')
    return redirect('list_patients')