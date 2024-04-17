from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from .forms import (
    UserCreationForm,
    UserChangeForm,
    AdminPasswordChangeForm,
)
from ..models import User
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    ordering = ('email',)
    search_fields = ['email', 'username']
    model = User
    form = UserChangeForm
    add_form_template = None
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    list_display = ['email', 'username']
    list_display_links = list_display
    readonly_fields = ['last_login', 'date_joined']
    fieldsets = (
        (
            _('Login informations'),
            {
                'fields': (
                    'email',
                    'username',
                    'password',
                )
            },
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                ),
            },
        ),
        (
            _('Important dates'),
            {
                'fields': (
                    'last_login',
                    'date_joined',
                )
            },
        ),
    )
    add_fieldsets = (
        (
            _('Login informations'),
            {
                'fields': (
                    'email',
                    'username',
                    'password1',
                    'password2',
                ),
            },
        ),
    )
