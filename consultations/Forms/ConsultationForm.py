from django.forms import ModelForm, CharField, HiddenInput

from consultations.Models.Consultation import Consultation


class ConsultationForm(ModelForm):

    class Meta:
        model = Consultation
        exclude = {'payment'}
        labels = {
            'date': 'Data da Consulta',
            'startTime': 'Hora de Inicio',
            'endTime': 'Hora de Término',
            'description': 'Descrição',
            'backgroundColor': 'Cor do evento na agenda',
            'textColor': ' Cor do texto do Evento'
        }
        widgets = {
            'patient': HiddenInput(),
            'procedure': HiddenInput()
        }
