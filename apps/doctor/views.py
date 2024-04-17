from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from accounts.views import HtmxBaseView

from .forms import DoctorRegisterForm
from .models import Specialties


@method_decorator(login_required, name='dispatch')
class DoctorRegister(HtmxBaseView):
    template_name = 'doctor_register.html'
    form_class = DoctorRegisterForm

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'doctor_register_form': self.form_class(),
            'specialties': Specialties.objects.all(),
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
