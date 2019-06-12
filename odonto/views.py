from django.shortcuts import render


def schedule(request):
    return render(request, 'dashboard/views/schedule.html', {"calendar": 'consultas'})

