from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.serializers import json
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from collections import OrderedDict

import calendar
from datetime import datetime, date, timedelta

# Create your views here.
from .models import Cost
from .models import Plots
from .models import PatientFinancial
from .forms import CostForm
from .forms import PlotForm

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
        
    costs = Cost.objects.all()
    financier = {"input": 0, "output": 0, "opened": 0, "balance": 0}
    all = {}
    monthly_plots_pay = Plots.objects.filter(paid_day__range=[begin, end])
    monthly_plots = Plots.objects.filter(paid_day=None, date__range=[begin, end])
    monthly_costs = Cost.objects.filter(cost_type=True)
    for cost in monthly_costs:
        cost_as_plot = cost.as_plot(year, month)
        if not cost_as_plot.paid_day:
            if not (cost_as_plot.date in all.keys()):
                all[cost_as_plot.date] = []
            all[cost_as_plot.date].append(cost_as_plot)
        else:
            if not (cost_as_plot.date in all.keys()):
                all[cost_as_plot.paid_day] = []
            all[cost_as_plot.paid_day].append(cost_as_plot)


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
                    if datetime.date(begin) < plot.paid_day < datetime.date(end):
                        financier["output"] = financier["output"] + plot.price
                else:
                    financier["opened"] = financier["opened"] - plot.price
    financier["balance"] = financier["input"]-financier["output"]

    if request.method == "GET" and request.is_ajax():
        data = []
        for cost in costs:
            data.append(cost.as_dict())
        return JsonResponse(data, safe=False)
    return render(request, 'accounting/list.html', {'costs': costs, 'all': all, "financier": financier, 'today': date.today(), 'year': year, 'month': month})

@login_required
def edit_plot(request, id):
    plot=  Plots.objects.get(pk=id)
    old_plot_price= plot.price
    form = PlotForm(request.POST or None, request.FILES or None, instance=plot)
    if request.method =="POST" and form.is_valid():
        patient_financial = plot.patient_financial
        plot = form.save()
        if plot.price==0:
            patient_financial.amount-=old_plot_price
            if plot.input:
                patient_financial.amount_paid=0
            plot.delete()
            patient_financial.num_plots-=1
            patient_financial.save()
            messages.add_message(request, messages.SUCCESS, 'Parcela Excluida Pois o Valor Estava Zerado!')
            return redirect('view_schedules', id=plot.patient_financial.consultation.id)

        if plot.price>old_plot_price:
            diff = plot.price-old_plot_price
            patient_financial.amount+=diff
        else:
            diff= old_plot_price-plot.price
            patient_financial.amount-=diff
        # print("Valor Antigo da Parcela:"+str(old_plot_price))
        # print("Valor Atual da Parcela:"+str(plot.price))
        # print("Diferença:"+str(diff))
        if plot.input:
            patient_financial.amount_paid=plot.price
        patient_financial.save()
        messages.add_message(request, messages.SUCCESS, 'Valor da Parcela Alterado!')
        return redirect('view_schedules', id=plot.patient_financial.consultation.id)
    return render(request, 'plots/edit.html', {'form': form,'consultation_id':plot.patient_financial.consultation.id})

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
def pay_plot(request, location, id, year=None, month=None):
    patient_financier = None
    if location == "consultation" or location == "financier":
        plot = Plots.objects.get(pk=id)
        plot.pay(datetime.now().date())
        messages.add_message(request, messages.SUCCESS, 'Pagamento da Parcela Realizado!')
        if plot.patient_financial:
            patient_financier = PatientFinancial.objects.get(pk=plot.patient_financial.id)
    else:
        cost = Cost.objects.get(pk=id)
        plot = cost.as_plot(year, month)
        plot.pay(datetime.now())
    if "financier" in location:
        return redirect('list_costs')
    return redirect('view_schedules', id=patient_financier.consultation.id)

@login_required
def delete_cost(request, id):
    cost = Cost.objects.get(pk=id)
    if cost.delete():
        messages.add_message(request, messages.SUCCESS, 'Custo Deletado!')
    return redirect('list_costs')