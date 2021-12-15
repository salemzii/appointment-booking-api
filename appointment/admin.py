from django.contrib import admin
from .models import Appointment, TimeSlot, Schedule

admin.site.register(Appointment)
admin.site.register(TimeSlot)
admin.site.register(Schedule)

# Register your models here.
