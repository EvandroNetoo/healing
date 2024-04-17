from django import forms
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from crispy_forms.layout import Layout, Row, Column, Submit, HTML, Div
from crispy_forms.helper import FormHelper
from crispy_bootstrap5.bootstrap5 import FloatingField

from .models import DoctorData


class DoctorRegisterForm(forms.ModelForm):
    class Meta:
        model = DoctorData
        exclude = ('user',)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].required = True
            self.fields[field].widget.attrs.update(
                {'class': 'shadow-main-color'}
            )
        self.fields['specialty'].required = False

        self.fields['crm'].widget.attrs['autofocus'] = True

        self.helper = FormHelper()

        self.helper.form_id = 'form'
        self.helper.attrs = {
            'hx-post': reverse_lazy('doctor_register'),
            'hx_target': '#form',
            'hx-swap': 'outerHTML',
        }

        submit = Submit('submit', _('Submit'))
        submit.field_classes = 'btn btn-success btn-dark-color'
        submit.attrs = {}

        self.helper.layout = Layout(
            Row(
                Column(FloatingField('crm')),
                Column(FloatingField('digital_crm')),
            ),
            FloatingField('name'),
            Row(
                Column(FloatingField('zip_code')),
                Column(FloatingField('street')),
            ),
            Row(
                Column(FloatingField('neighborhood')),
                Column(FloatingField('number')),
            ),
            Row(
                Column(FloatingField('rg')),
                Column(FloatingField('photo')),
            ),
            Row(
                Column(FloatingField('specialty')),
                Column(FloatingField('consultation_fee')),
            ),
            FloatingField('description'),
            submit,
        )
