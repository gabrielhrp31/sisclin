from django.forms import ModelForm, CharField, HiddenInput

from consultations.Models.Consultation import Consultation


class ConsultationForm(ModelForm):
    title = CharField(label="Titulo")

    class Meta:
        model = Consultation
        exclude = {'payment'}
        labels = {
            'start': 'Data de Inicio',
            'startTime': 'Hora de Inicio',
            'end': 'Data de Término',
            'endTime': 'Hora de Término',
            'allDay': 'Durará o dia todo',
            'description': 'Descrição',
            'holiday': 'Evento ou Feriado',
            'backgroundColor': 'Cor do evento na agenda',
            'textColor': ' Cor do texto do Evento'
        }
        widgets = {
            'patient': HiddenInput()
        }
