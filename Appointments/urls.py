"""Appointments URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from appointment import views
from django.contrib.auth import views as authviews


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('bookappointment/<str:invitee_name>', views.bookappointment, name='book'),
    path('createTimeSlot/<int:userId>', views.create_timeslot, name='timeslot'),
    path('timeslots/<int:userId>', views.view_timeSlots, name='timeslots'),
    path('setschedule/<int:timeslotId>', views.setSchedule, name='setschedule'),
    path('appointments/<int:userId>', views.booked_appointments, name='bookedappointments'),
    path('invitations/<int:userId>', views.invited_appointments, name='invitations'),
    path('cancel/<int:appointmentId>', views.cancel_appointment, name='cancel'),
    path('approve/<int:appointmentId>', views.approve_appointment, name='approve'),
    path('check', views.check),
    path('login', authviews.LoginView.as_view(template_name='admin/login.html'), name='login'),
    path('logout', authviews.LogoutView.as_view(template_name='logout.html'), name='logout'),
 
]
