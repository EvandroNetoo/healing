from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from accounts.decorators import doctor_required, not_doctor_required
from accounts.views import HtmxBaseView

from .forms import DoctorRegisterForm, OpenScheduleForm
from .models import OpenedDate


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
