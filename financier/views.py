from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.serializers import json
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from .models import Cost
from .models import Plots
from .forms import CostForm


def index(request):
    return render(request, 'financier.html')


@login_required
def list_costs(request):
    costs = Cost.objects.all()
    if request.method == "GET" and request.is_ajax():
        data = []
        for cost in costs:
            data.append(cost.as_dict())
        return JsonResponse(data, safe=False)
    return render(request, 'accounting/list.html', {'costs': costs})


@login_required
def new_cost(request):
    cost_form = CostForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if cost_form.is_valid():
            cost = cost_form.save()
            plots = Plots()
            if cost.payment_form:
                plots.created(cost.amount, 0, cost.num_plots, None)
            else:
                plots.created(cost.amount, 0, cost.num_plots, cost.payday)
            plots.save()
            cost.plots = plots
            cost.save()
            messages.add_message(request, messages.SUCCESS, 'Lançamento Cadastrado')
            return redirect('list_costs')
    return render(request, 'accounting/new.html', {'cost_form': cost_form})
