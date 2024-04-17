from django.urls import path
from .views import *

urlpatterns = [
    path('doctor_register/', DoctorRegister.as_view(), name='doctor_register'),
]
