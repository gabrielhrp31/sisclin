from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from .forms import PatientForm


def index(request):
    return render(request, 'patients.html')


@login_required
def list_patients(request):
    return render(request, 'patients/list.html')


@login_required
def new_patient(request):
    patient_form = PatientForm(request.POST or None, request.FILES or None)
    return render(request, 'patients/new.html', {'patient_form': patient_form})
