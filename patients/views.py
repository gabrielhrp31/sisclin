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
from .models import Address
from .models import Patient
from .models import Photo
from consultations.models import Consultation
from .forms import PhotoForm
from .forms import AddressForm
from .forms import PatientForm


@login_required
def list_patients(request):
    patients = Patient.objects.all()
    if request.method == "GET" and request.is_ajax():
        data = []
        for patient in patients:
            data.append(patient.as_dict())
        return JsonResponse(data, safe=False)
    return render(request, 'patients/list.html', {'patients': patients})


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
    consultations_timeline = {}
    patient = Patient.objects.get(pk=id)
    photos_list = Photo.objects.all()
    if request.is_ajax() and request.method == "GET":
        data = patient.as_dict()
        return JsonResponse(data, safe=False)
    elif request.method == "DELETE":
        data = request.body.decode().split('=')
        photo = Photo.objects.get(pk=data[1])
        photo.delete()
        return JsonResponse({'message': 'Imagem Apagada com Sucesso'}, safe=False)
    elif request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.patient = patient
            photo.title = photo.file.name.replace('photos/', '')
            photo.save()
            data = {'is_valid': True, 'id': photo.id ,'name': photo.title, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
    else:
        consultations = Consultation.objects.filter(patient=id)
        for consultation in consultations:
            if not (consultation.date in consultations_timeline.keys()):
                consultations_timeline[consultation.date] = []
                consultations_timeline[consultation.date].append(consultation)
            else:
                consultations_timeline[consultation.date].append(consultation)
        consultations_timeline = OrderedDict(sorted(consultations_timeline.items(), key=lambda t: t[0], reverse=True))
    return render(request, 'patients/view.html', {'patient': patient, 'consultations': consultations_timeline, 'today': date.today(), 'photos': photos_list})


@login_required
def get_address(request):
    print('FUNCAO GET')
    addresses = Address.objects.all()
    if request.is_ajax():
        data = []
        for address in addresses:
            data.append(address.as_dict())
        return JsonResponse(data, safe=False)
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