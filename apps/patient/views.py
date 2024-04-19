from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.db import transaction

from datetime import datetime, timedelta

from accounts.decorators import doctor_required
from accounts.views import HtmxBaseView
from doctor.models import DoctorData, OpenedDate
from doctor.models import Specialties

from .models import Appointment, Document


@method_decorator([login_required], name='dispatch')
class HomeView(HtmxBaseView):
    template_name = 'home.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        doctors = DoctorData.objects.all()
        specialties = Specialties.objects.all()

        doctor_filter = request.GET.get('doctor')
        specialties_filter = request.GET.getlist('specialties')

        if doctor_filter:
            doctors = doctors.filter(nome__icontains=doctor_filter)

        if specialties_filter:
            doctors = doctors.filter(specialty_id__in=specialties_filter)

        context = {
            'doctors': doctors,
            'specialties': specialties,
        }
        return render(request, self.template_name, context)


@method_decorator([login_required], name='dispatch')
class ChooseScheduleView(HtmxBaseView):
    template_name = 'choose_schedule.html'

    def get(self, request, doctor_data_id):
        if request.method == 'GET':
            doctor = DoctorData.objects.get(id=doctor_data_id)
            opened_dates = (
                OpenedDate.objects.filter(user=doctor.user)
                .filter(date__gte=datetime.now())
                .filter(scheduled=False)
            )
            return render(
                request,
                'choose_schedule.html',
                {'doctor': doctor, 'opened_dates': opened_dates},
            )


@method_decorator([login_required, transaction.atomic], name='dispatch')
class ScheduleAppointment(HtmxBaseView):
    def get(self, request, opened_date_id):
        data_aberta = get_object_or_404(OpenedDate, id=opened_date_id)

        Appointment.objects.create(
            patient=request.user, opened_date=data_aberta
        )

        data_aberta.scheduled = True
        data_aberta.save()

        messages.success(request, _('Successfully scheduled appointment.'))

        return redirect('my_appointments')


@method_decorator([login_required], name='dispatch')
class MyAppointmentsView(HtmxBaseView):
    template_name = 'my_appointments.html'

    def get(self, request):

        my_appointments = Appointment.objects.filter(
            patient=request.user,
            opened_date__date__gte=datetime.now(),
        )

        context = {
            'my_appointments': my_appointments,
        }

        return render(request, self.template_name, context)


@method_decorator([login_required], name='dispatch')
class AppointmentView(HtmxBaseView):
    template_name = 'patient_appointment.html'

    def get(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, id=appointment_id)
        doctor_data = DoctorData.objects.get(user=appointment.opened_date.user)
        documents = Document.objects.filter(appointment=appointment)

        context = {
            'appointment': appointment,
            'doctor_data': doctor_data,
            'documents': documents,
        }

        return render(request, self.template_name, context)
