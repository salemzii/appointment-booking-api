from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Appointment, TimeSlot, Schedule
import datetime
from .forms import TimeSlotForm
from .decorators import is_loggedIn

amqp = 'amqps://krfnnecp:cQPGvECO9rsqgpzfqmBHA2OT9WNnUVJG@jaguar.rmq.cloudamqp.com/krfnnecp'


def bookappointment(request, invitee_name):
    invited = User.objects.get(username=invitee_name)
    slots = getinvitedUserAvailableTimeSlots(invitee_name)

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

    return render(request, 'bookappointment.html', {'slots': slots, 'invitee': invited})


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



def view_timeSlots(request, userId):
    user = User.objects.get(id=userId)
    timeslots = TimeSlot.objects.filter(user=user)
    return render(request, 'timeslots.html', {'timeslots': timeslots})


def setSchedule(request, timeslotId):
    timeslot = TimeSlot.objects.get(id=timeslotId)
    
    data = {}
    print('Preparing data.....')
    if request.method == "POST":
        print('Passed here!')
        if request.user == timeslot.user:
            data['occupied'] = request.POST.get('occupied', True)
            occupied = bool(data['occupied'])
            data['day'] = request.POST['day']
            print("passed second if block!")

            try:
                create = Schedule.objects.create(
                    time_slot= timeslot,
                    occupied= occupied,
                    day= data['day']
                )
                create.save()
                print('Prepared succesffully!')
                return redirect(reverse('timeslots', args=[request.user.id]))
            except Exception as err:
                messages.error(request, f"Encountered {err}")
        else:
            pass

    return render(request, 'setSchedule.html')



def getinvitedUserAvailableTimeSlots(invitedUser):
    invited = User.objects.get(username=invitedUser) #get invited user 
    invitedTimeSlots = invited.time_slot.all()
    invitedAvailableTimeSlot = []
    date = datetime.datetime.now()

    for slot in invitedTimeSlots:
        try:
            schedule = Schedule.objects.get(time_slot=slot)
            if schedule.occupied == False:
                invitedAvailableTimeSlot.append(str(slot))
        
            elif schedule.occupied == False and schedule.day != date.day():
                invitedAvailableTimeSlot.append(str(slot))
            else:
                pass
        except Exception as err:
            invitedAvailableTimeSlot.append(str(slot))

    return invitedAvailableTimeSlot




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


def cancel_appointment(request, appointmentId):
    appointment = Appointment.objects.get(id=appointmentId)
    
    if appointment.inviter == request.user or appointment.invitee == request.user:
        appointment.approved = False
        appointment.save()
        messages.success(request, f"Appointment {appointment.title} cancelled!")
        return redirect(reverse('bookedappointments', args=[request.user.id]))
    messages.error(request, f"You are not allowed to cancel this appointment!")
    return redirect(reverse('bookedappointments', args=[request.user.id])) 


def check(request):
    val = {}
    print((request.path.capitalize()))
    if request.method == "POST":
        title = request.POST['title']
        print(title)
    return render(request, 'check.html')
 