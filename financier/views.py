from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.serializers import json
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from collections import OrderedDict

import calendar
from datetime import datetime, date

# Create your views here.
from .models import Cost
from .models import Plots
from .models import PatientFinancial
from .forms import CostForm


def index(request):
    return render(request, 'financier.html')


@login_required
def list_costs(request, year=None, month=None):
    begin = end = None
    if not year and not month:
        range = calendar.monthrange(datetime.now().year, datetime.now().month)
        begin = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end = datetime.now().replace(day=range[1], hour=0, minute=0, second=0, microsecond=0)
    else:
        range = calendar.monthrange(year, month)
        begin = datetime.now().replace(day=1, month=month, year=year, hour=0, minute=0, second=0, microsecond=0)
        end = datetime.now().replace(day=range[1], month=month, year=year, hour=0, minute=0, second=0, microsecond=0)
        print(begin)
        print (end)
        
    costs = Cost.objects.all()
    financier = {"input": 0, "output": 0, "opened": 0, "balance": 0}
    all = {}
    monthly_plots_pay = Plots.objects.filter(paid_day__range=[begin, end])
    monthly_plots = Plots.objects.filter(paid_day=None, date__range=[begin, end])
    monthly_costs = Cost.objects.filter(Q(payday__range=[begin, end]), cost_type=True)
    for cost in monthly_costs:
        if not (cost.payday in all.keys()):
            all[cost.payday] = []
        if not cost.get_payment_date():
            all[cost.payday].append(cost.as_plot())

    # print(monthly_costs)
    for plot in monthly_plots_pay:
        if not (plot.paid_day in all.keys()):
            all[plot.paid_day] = []
        all[plot.paid_day].append(plot)
    for plot in monthly_plots:
        if not (plot.date in all.keys()):
            all[plot.date] = []
        all[plot.date].append(plot)
    all = OrderedDict(sorted(all.items(), key=lambda t: t[0], reverse=True))
    # print(all)
    for value in all.values():
        for plot in value:
            if plot.type == 1:
                if plot.paid_day:
                    financier["input"] = financier["input"]+plot.price
                else:
                    financier["opened"] = financier["opened"] + plot.price
            else:
                if plot.paid_day:
                    financier["output"] = financier["output"] + plot.price
                else:
                    financier["opened"] = financier["opened"] + plot.price
    financier["balance"] = financier["input"]-financier["output"]

    if request.method == "GET" and request.is_ajax():
        data = []
        for cost in costs:
            data.append(cost.as_dict())
        return JsonResponse(data, safe=False)
    return render(request, 'accounting/list.html', {'costs': costs, 'all': all, "financier": financier, 'today': date.today()})


@login_required
def new_cost(request):
    cost_form = CostForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if cost_form.is_valid():
            cost = cost_form.save()
            if not cost.cost_type:
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
            else:
                cost.payday.replace(month=datetime.now().month)
                cost.save()
            return redirect('list_costs')
    return render(request, 'accounting/new.html', {'cost_form': cost_form})


@login_required
def pay_plot(request, location, id):
    patient_financier = None
    if location == "consultation" or location == "financier":
        plot = Plots.objects.get(pk=id)
        plot.pay(datetime.now().date())
        messages.add_message(request, messages.SUCCESS, 'Pagamento da Parcela Realizado!')
        patient_financier = PatientFinancial.objects.get(pk=plot.patient_financial.id)
    else:
        cost = Cost.objects.get(pk=id)
        plot = cost.as_plot()
        plot.pay(datetime.now())
    if "financier" in location:
        return redirect('list_costs')
    return redirect('view_schedules', id=patient_financier.consultation.id)

def delete_cost(request, id):
    cost = Cost.objects.get(pk=id)
    if cost.delete():
        messages.add_message(request, messages.SUCCESS, 'Custo Deletado!')
    return redirect('list_costs')