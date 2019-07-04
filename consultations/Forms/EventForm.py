from django.forms import ModelForm, CharField

from consultations.Models.Event import Event


class EventForm(ModelForm):
    title = CharField(label="Título")

    class Meta:
        model = Event
        fields = '__all__'
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
