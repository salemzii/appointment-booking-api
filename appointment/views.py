from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Appointment, TimeSlot
import datetime


def bookappointment(request, invitee_name):
    invited = User.objects.get(username=invitee_name)
    invitedTimeSlots = invited.time_slot.all()
    invitedTimeSlot = [str(slot) for slot in invitedTimeSlots if slot.occupied == False]

    if request.method == "POST":
        data = {}
        data['title'] = request.POST['title']
        data['context'] = request.POST['context']
        data['date'] = request.POST['date']
        data['timeslot'] = request.POST['slot']
        raw_slot = invited.time_slot.get(time=data['timeslot'])

        invited_appointments = Appointment.objects.filter(invitee=invited)
        date_object = data['date'] +" "+ data['timeslot']
        day = datetime.datetime.strptime(date_object, '%Y-%m-%d %H:%M:%S')
        check_ls = []

        for appointment in invited_appointments:
            dt = f"{appointment.date} {appointment.time_slot.time}"
            if datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S') != day:
                check_ls.append(True)               
            else:
                check_ls.append(False)
        
        if all(check_ls):
            try:
                save_appointment = Appointment.objects.create(
                    title= data['title'],
                    context= data['context'], 
                    time_slot= raw_slot,  
                    date= data['date'],
                    inviter= request.user,
                    invitee= invited
                )
                save_appointment.save()
                messages.success(request, f"Your appointment with {invited.username} has been placed successfully")
            except Exception as err:
                messages.error(request, f"Unable to place your appointment at the moment.")
                print(err)            
        else:
            messages.error(request, f"Unable to place appointment, time slot occupied already!")
            print("Slot occupied!")
            
    else:
        pass

    return render(request, 'bookappointment.html', {'slots': invitedTimeSlot, 'invitee': invited})


def create_timeslot(request, userId):
    user = User.objects.get(id=userId)
    if request.method == "POST":
        data = {}

        


def check(request):
    val = {}
    if request.method == "POST":
        title = request.POST['title']
        print(title)
    return render(request, 'check.html')
