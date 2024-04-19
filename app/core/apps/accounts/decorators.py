from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.contrib import messages

from functools import wraps


def doctor_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_doctor:
            messages.error(
                request, _('To access this page you need to be a doctor.')
            )
            return redirect('doctor_register')
        return view_func(request, *args, **kwargs)

    return wrapper


def not_doctor_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_doctor:
            messages.error(
                request,
                _('You have already completed your medical registration.'),
            )
            return redirect('open_schedule')
        return view_func(request, *args, **kwargs)

    return wrapper
