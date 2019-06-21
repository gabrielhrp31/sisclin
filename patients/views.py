from django.contrib.auth.decorators import login_required
from django.core.serializers import json
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from .models import Address
from .forms import AddressForm
from .forms import PatientForm


def index(request):
    return render(request, 'patients.html')


@login_required
def list_patients(request):
    return render(request, 'patients/list.html')


@login_required
def new_patient(request):
    patient_form = PatientForm(request.POST or None, request.FILES or None)
    address_form = AddressForm(request.POST or None, request.FILES or None)
    return render(request, 'patients/new.html', {'patient_form': patient_form, 'address_form':address_form})


@login_required
def new_address(request):
    if request.method == "POST" and request.is_ajax():
        address = Address(number=request.POST['number'], city=request.POST['city'], country=request.POST['country'], postal_code=request.POST['postal_code'], street=request.POST['street'])
        address.save()
        data = dict({'success': True, 'message': 'Endereço Criado com Sucesso', 'data': [address.id, request.POST] })
        return JsonResponse(data)
    data = dict({'success': False, 'message': 'Erro'})
    return JsonResponse(data)


@login_required
def get_address(request):
    address = Address.objects.all()
    data = []
    for address in address:
        data.append(address.as_dict())
    return JsonResponse(data, safe=False)
