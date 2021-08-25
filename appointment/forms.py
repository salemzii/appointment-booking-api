from django import forms
from .models import Appointment, TimeSlot


class AppointmentForm(forms.ModelForm):

    class meta:
        model = Appointment
        fields = ['title', 'date', 'time_slot', 'context']
        

