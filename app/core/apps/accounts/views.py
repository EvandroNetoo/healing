from django.template.context_processors import csrf
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.forms import Form, ModelForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views import View

from crispy_forms.utils import render_crispy_form

from .forms import UserRegisterForm, UserLoginForm
from .models import User


class HtmxBaseView(View):
    def rendered_form(
        self,
        request: HttpRequest,
        form: Form | ModelForm,
    ) -> HttpResponse:

        context = {}
        context.update(csrf(request))
        form_html = render_crispy_form(form, form.helper, context)
        return HttpResponse(form_html)

    def htmx_redirect(self, url: str, *args, **kwargs):
        resp = HttpResponse('')
        resp['HX-Redirect'] = reverse_lazy(url, *args, **kwargs)
        return resp

    def login_and_htmx_redirect(
        self,
        request: HttpRequest,
        user: User,
        remember_me: bool = False,
    ) -> HttpResponse:

        login(request, user)
        if not remember_me:
            request.session.set_expiry(0)

        if user.is_doctor:
            return self.htmx_redirect('open_schedule')
        return self.htmx_redirect('doctor_register')


class RegisterView(HtmxBaseView):
    form_class = UserRegisterForm
    template_name = 'register.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'register_form': self.form_class(),
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = self.form_class(request.POST)

        if not form.is_valid():
            return self.rendered_form(request, form)

        user = form.save()

        return self.login_and_htmx_redirect(
            request, user, form.cleaned_data['remember_me']
        )


class LoginView(HtmxBaseView):
    form_class = UserLoginForm
    template_name = 'login.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'login_form': self.form_class(),
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = self.form_class(request.POST)

        if not form.is_valid():
            return self.rendered_form(request, form)

        return self.login_and_htmx_redirect(
            request, form.user, form.cleaned_data['remember_me']
        )


class LogoutView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        logout(request)
        return redirect('login')
