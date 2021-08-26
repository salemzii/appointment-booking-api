from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Appointment, TimeSlot
import datetime
from .forms import TimeSlotForm



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

        data['name'] = request.POST['name']
        data['time'] = request.POST['time']
        data['occupied'] = request.POST.get('occupied', False)
        occupied = bool(data['occupied'])
        print(occupied)

        try:
            create = TimeSlot.objects.create(
                user = user,
                time= data['time'],
                name= data['name'],
                occupied = occupied
            )
            create.save()
        
        except Exception as err:
            messages.error(request, f"Encountered {err}")


    return render(request, 'createTimeSlot.html')


def booked_appointments(request, userId):
    user = User.objects.get(id=userId)
    appointments = user.inviter.all()
    approved = [appointment for appointment in appointments if appointment.approved == True]
    return render(request, 'bookedappointments.html', {'appointments': approved})


def invited_appointments(request, userId):
    user = User.objects.get(id=userId)
    invites = user.invitee.all()
    appointments = [invite for invite in invites if invite.approved == False ]
    return render(request, 'invitedappointments.html', {"appointments": appointments})


def approve_appointment(request, appointmentId):
    appointment = Appointment.objects.get(id=appointmentId)
    if appointment.invitee == request.user:
        appointment.approved = True
        appointment.save()
        messages.success(request, f"Appointment approved")
        return redirect(reverse('bookedappointments', args=[request.user.id]))
    messages.error(request, f"You are not allowed to approve this appointment!")
    return redirect(reverse('bookedappointments', args=[request.user.id]))
 

def check(request):
    val = {}
    if request.method == "POST":
        title = request.POST['title']
        print(title)
    return render(request, 'check.html')
