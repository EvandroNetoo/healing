from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from django.urls import reverse_lazy
from django import forms

from crispy_forms.layout import Layout, Row, Column, Submit, HTML, Div
from crispy_forms.helper import FormHelper
from crispy_bootstrap5.bootstrap5 import FloatingField

from .models import User


class PasswordForm(forms.Form):
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(),
        validators=User.password_validators,
    )

    password2 = forms.CharField(
        label=_('Confirm password'),
        widget=forms.PasswordInput(),
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_('Passwords does not match.'))

        return password2


class UserRegisterForm(forms.ModelForm, PasswordForm):
    class Meta:
        model = User
        fields = ('email', 'username')

    remember_me = forms.BooleanField(label=_('Remember me?'))

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].required = True
        self.fields['remember_me'].required = False

        self.fields['email'].widget.attrs['autofocus'] = True

        self.helper = FormHelper()

        self.helper.form_id = 'form'
        self.helper.attrs = {
            'hx-post': reverse_lazy('register'),
            'hx_target': '#form',
            'hx-swap': 'outerHTML',
        }

        submit = Submit('submit', _('Submit'))
        submit.field_classes = 'btn btn-success btn-dark-color'
        submit.attrs = {}

        self.helper.layout = Layout(
            FloatingField('email'),
            FloatingField('username'),
            Row(
                Column(FloatingField('password1')),
                Column(FloatingField('password2')),
            ),
            'remember_me',
            Div(
                submit,
                HTML(
                    f'<a href="{reverse_lazy("login")}" class="btn btn-dark-color-outline">Já possuo uma conta</a>'
                ),
                css_class='d-flex justify-content-between',
            ),
        )

    def clean_email(self):
        return self.cleaned_data['email'].lower()

    def save(self, commit: bool = True) -> User:
        user = User(
            email=self.cleaned_data['email'],
            username=self.cleaned_data['username'],
        )
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email_username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    remember_me = forms.BooleanField(label=_('Remember me?'))

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].required = True
        self.fields['remember_me'].required = False

        self.fields['email_username'].widget.attrs['autofocus'] = True

        self.helper = FormHelper()

        self.helper.form_id = 'form'
        self.helper.attrs = {
            'hx-post': reverse_lazy('login'),
            'hx_target': '#form',
            'hx-swap': 'outerHTML',
        }

        submit = Submit('submit', _('Submit'))
        submit.field_classes = 'btn btn-success btn-dark-color'
        submit.attrs = {}

        self.helper.layout = Layout(
            FloatingField('email_username'),
            FloatingField('password'),
            'remember_me',
            Div(
                submit,
                HTML(
                    f'<a href="{reverse_lazy("register")}" class="btn btn-dark-color-outline">Não possuo uma conta</a>'
                ),
                css_class='d-flex justify-content-between',
            ),
        )

    def clean_email_username(self):
        return self.cleaned_data['email_username'].lower()

    def clean(self):
        self.user = authenticate(
            username=self.cleaned_data.get('email_username'),
            password=self.cleaned_data.get('password'),
        )

        if (
            not self.user
            and self.cleaned_data.get('email_username')
            and self.cleaned_data.get('password')
        ):
            self.add_error(None, _('Sorry, your password was incorrect.'))

        return super().clean()
