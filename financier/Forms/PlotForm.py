from django.forms import ModelForm
from financier.Models.Plots import Plots

class PlotForm(ModelForm):
    class Meta:
        model = Plots
        exclude = ['paid_day','status','input', 'type', 'cost', 'patient_financial']