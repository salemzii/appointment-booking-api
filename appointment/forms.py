from django import forms
from .models import Appointment, TimeSlot, Schedule


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ['title', 'date', 'time_slot', 'context']


class TimeSlotForm(forms.ModelForm):

    class Meta:
        model = TimeSlot
        fields = ['name', 'time']
        

class ScheduleForm(forms.ModelForm):

    class Meta:
        model = Schedule
        fields = ['occupied', 'day']


