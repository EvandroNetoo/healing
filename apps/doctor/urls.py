from django.urls import path
from .views import *

urlpatterns = [
    path(
        'doctor_register/',
        DoctorRegisterView.as_view(),
        name='doctor_register',
    ),
    path('open_schedule/', OpenScheduleView.as_view(), name='open_schedule'),
]
