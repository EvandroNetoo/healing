from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.http import HttpRequest, HttpResponse
from django.utils.translation import gettext_lazy
from django.contrib import messages

from datetime import datetime, timedelta

from accounts.decorators import doctor_required, not_doctor_required
from accounts.views import HtmxBaseView
from patient.models import Appointment, Document

from .forms import DoctorRegisterForm, OpenScheduleForm
from .models import OpenedDate, DoctorData


@method_decorator([login_required, not_doctor_required], name='dispatch')
class DoctorRegisterView(HtmxBaseView):
    template_name = 'doctor_register.html'
    form_class = DoctorRegisterForm

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'doctor_register_form': self.form_class(),
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = self.form_class(request.POST, request.FILES)

        if not form.is_valid():
            return self.rendered_form(request, form)

        doctor = form.save(commit=False)
        doctor.user = request.user
        doctor.save()

        return self.htmx_redirect('doctor_register')


@method_decorator([login_required, doctor_required], name='dispatch')
class OpenScheduleView(HtmxBaseView):
    template_name = 'open_schedule.html'
    form_class = OpenScheduleForm

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'open_schedule_form': self.form_class(),
            'opened_dates': OpenedDate.objects.filter(user=request.user),
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = self.form_class(request.POST, request.FILES)

        if not form.is_valid():
            return self.rendered_form(request, form)

        open_date = form.save(commit=False)
        open_date.user = request.user
        open_date.save()

        return self.htmx_redirect('open_schedule')


@method_decorator([login_required, doctor_required], name='dispatch')
class DoctorAppointments(HtmxBaseView):
    template_name = 'doctor_appointments.html'

    def get(self, request: HttpRequest) -> HttpResponse:

        today = datetime.now().date()

        today_appointments = Appointment.objects.filter(
            opened_date__user=request.user,
            opened_date__date__gte=today,
            opened_date__date__lt=today + timedelta(days=1),
        )
        others_appointments = Appointment.objects.exclude(
            id__in=today_appointments.values('id'),
        )
        context = {
            'today_appointments': today_appointments,
            'others_appointments': others_appointments,
        }
        return render(request, 'doctor_appointments.html', context)


from django.utils.translation import gettext_lazy as _

@method_decorator([login_required, doctor_required], name='dispatch')
class AppointmentView(HtmxBaseView):
    template_name = 'doctor_appointment.html'

    def get(self, request: HttpRequest, appointment_id: int) -> HttpResponse:
        appointment = get_object_or_404(Appointment, id=appointment_id)
        doctor_data = DoctorData.objects.get(user=appointment.opened_date.user)
        documents = Document.objects.filter(appointment=appointment)

        context = {
            'appointment': appointment,
            'doctor_data': doctor_data,
            'documents': documents,
        }

        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, appointment_id: int) -> HttpResponse:
        appointment = get_object_or_404(Appointment, id=appointment_id)
        link = request.POST.get('link')

        if appointment.status == 'C':
            messages.warning(
                request,
                _('This appointment has already been canceled, you cannot start it.'),
            )
            return redirect(
                'doctor_appointment', appointment_id=appointment_id
            )
        elif appointment.status == 'F':
            messages.warning(
                request,
                _('This appointment has already been finished, you cannot start it.'),
            )
            return redirect(
                'doctor_appointment', appointment_id=appointment_id
            )

        appointment.link = link
        appointment.status = 'I'
        appointment.save()

        messages.success(request, _('Consultation started successfully.'))
        return redirect('doctor_appointment', appointment_id=appointment_id)


@method_decorator([login_required, doctor_required], name='dispatch')
class AddDocumentView(HtmxBaseView):
    def post(self, request: HttpRequest, appointment_id: int) -> HttpResponse:
        appointment = get_object_or_404(Appointment, id=appointment_id)

        if appointment.opened_date.user != request.user:
            messages.error(request, _('This is not your appointment!'))
            return redirect(
                'doctor_appointment', appointment_id=appointment_id
            )

        title = request.POST.get('titulo')
        document = request.FILES.get('documento')

        if not document:
            messages.warning(request, _('Add the document.'))
            return redirect(
                'doctor_appointment', appointment_id=appointment_id
            )

        document = Document(
            appointment=appointment, title=title, document=document
        )

        document.save()

        messages.success(request, _('Document sent successfully!'))
        return redirect('doctor_appointment', appointment_id=appointment_id)

