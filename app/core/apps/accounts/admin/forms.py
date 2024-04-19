from django import forms
from django.contrib.auth import forms as auth_forms
from ..models import User
from accounts.validators import *
from django.utils.translation import gettext_lazy as _
from ..models import User
from ..forms import PasswordForm


class UserCreationForm(forms.ModelForm, PasswordForm):
    class Meta:
        model = User
        fields = ['email']

    def save(self, commit: bool = True):
        self.instance.set_password(self.cleaned_data.get('password1'))
        return super().save(commit)


class AdminPasswordChangeForm(PasswordForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        """Save the new password."""
        password = self.cleaned_data['password1']
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

    @property
    def changed_data(self):
        data = super().changed_data
        for name in self.fields:
            if name not in data:
                return []
        return ['password']


class UserChangeForm(auth_forms.UserChangeForm):
    class Meta(auth_forms.UserChangeForm):
        model = User
        fields = '__all__'
