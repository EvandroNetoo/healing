from django.urls import path
from .views import *

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path(
        'choose_schedule/<int:doctor_data_id>/',
        ChooseScheduleView.as_view(),
        name='choose_schedule',
    ),
    path(
        'schedule_appointment/<int:opened_date_id>/',
        ScheduleAppointment.as_view(),
        name='schedule_appointment',
    ),
    path(
        'my_appointments/',
        MyAppointmentsView.as_view(),
        name='my_appointments',
    ),
    path(
        'appointment/<int:appointment_id>',
        AppointmentView.as_view(),
        name='patient_appointment',
    ),
]
