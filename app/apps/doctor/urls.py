from django.urls import path
from .views import *

urlpatterns = [
    path(
        'doctor_register/',
        DoctorRegisterView.as_view(),
        name='doctor_register',
    ),
    path('open_schedule/', OpenScheduleView.as_view(), name='open_schedule'),
    path(
        'doctor_appointments/',
        DoctorAppointments.as_view(),
        name='doctor_appointments',
    ),
    path(
        'appointment/<int:appointment_id>',
        AppointmentView.as_view(),
        name='doctor_appointment',
    ),
    path(
        'add_document/<int:appointment_id>/',
        AddDocumentView.as_view(),
        name='add_document',
    ),
]
