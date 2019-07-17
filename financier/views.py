from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.serializers import json
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from collections import OrderedDict


from datetime import datetime, date

# Create your views here.
from .models import Cost
from .models import Plots
from .models import PatientFinancial
from .forms import CostForm


def index(request):
    return render(request, 'financier.html')


@login_required
def list_costs(request):
    costs = Cost.objects.all()
    all = {}
    monthly_plots_pay = Plots.objects.filter(paid_day__gte=datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0))
    monthly_plots = Plots.objects.filter(paid_day=None, date__range=[datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0), datetime.now().replace(day=30, hour=0, minute=0, second=0, microsecond=0)])
    monthly_costs = Cost.objects.filter(Q(payday__range=[datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0), datetime.now().replace(day=30, hour=0, minute=0, second=0, microsecond=0)]) | Q(cost_type=True))
    print(monthly_costs)
    for plot in monthly_plots_pay:
        if not (plot.paid_day in all.keys()):
            all[plot.paid_day] = []
        all[plot.paid_day].append(plot)
    for plot in monthly_plots:
        if not (plot.date in all.keys()):
            all[plot.date] = []
        all[plot.date].append(plot)
    all = OrderedDict(sorted(all.items(), key=lambda t: t[0], reverse=True))
    print(all)
    if request.method == "GET" and request.is_ajax():
        data = []
        for cost in costs:
            data.append(cost.as_dict())
        return JsonResponse(data, safe=False)
    return render(request, 'accounting/list.html', {'costs': costs, 'all': all,  'today': date.today()})


@login_required
def new_cost(request):
    cost_form = CostForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if cost_form.is_valid():
            cost = cost_form.save()
            if cost.payment_form:
                plots = Plots()
                plots.create(cost.amount, cost.payday, cost, 2)
                if cost.status:
                    plots.pay(datetime.now())
            else:
                plots_price = cost.amount/cost.num_plots
                for i in range(0, cost.num_plots):
                    plots = Plots()
                    date = cost.payday + timedelta(days=(30 * (i + 1)))
                    plots.create(plots_price, date, cost, 2)
            messages.add_message(request, messages.SUCCESS, 'Lançamento Cadastrado')
            return redirect('list_costs')
    return render(request, 'accounting/new.html', {'cost_form': cost_form})


@login_required
def pay_plot(request, id):
    plot = Plots.objects.get(pk=id)
    plot.pay(datetime.now().date())
    messages.add_message(request, messages.SUCCESS, 'Pagamento da Parcela Realizado!')
    patient_financier = PatientFinancial.objects.get(pk=plot.patient_financial.id)
    return redirect('view_schedules', id=patient_financier.consultation.id)
