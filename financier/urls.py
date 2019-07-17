"""odonto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name="patients_index"),
    path('list', views.list_costs, name="list_costs"),
    path('list/<int:year>/<int:month>/', views.list_costs, name="list_costs_filtered"),
    path('new', views.new_cost, name="new_cost"),
    #PLOTS
    path('pay/<slug:location>/<int:id>/', views.pay_plot, name="pay_plot"),
    path('pay/<slug:location>/<int:id>/<int:year>/<int:month>/', views.pay_plot, name="pay_plot_fix")
]
