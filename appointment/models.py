from django.db import models
from django.contrib.auth.models import User
import datetime


def get_date():
    dT = datetime.datetime.now()
    date = datetime.datetime.date(dT)
    return date

class TimeSlot(models.Model):
    NAME_CHOICES = (
        ('morning', 'morning'), 
        ('midday', 'midday'),
        ('evening', 'evening')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="time_slot")
    name = models.CharField(
        choices=NAME_CHOICES, max_length=12)

    time = models.TimeField()
    occupied = models.BooleanField(default=False)

    def __str__(self):
        template = f"{self.time}"
        return template.format(self)


class Appointment(models.Model):

    title = models.CharField(max_length=50, default="I'd like to book an appoinment.")
    inviter = models.ForeignKey(User, 
            related_name='inviter', 
            on_delete=models.CASCADE)
    invitee = models.ForeignKey(User, 
            related_name='invitee', 
            on_delete=models.CASCADE)
    date = models.DateField(default=get_date)
    time_slot = models.ForeignKey(TimeSlot,
            related_name='timeslots',
            on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    context = models.TextField()

    def __str__(self):
        return self.title



# Create your models here.
