from django.utils.translation import gettext_lazy as _
from django.apps import apps
from django.db import models

from accounts.models import User
from datetime import datetime

from .validators import cep_validator


class Specialties(models.Model):
    specialty = models.CharField(_('Specialty'), max_length=100)
    icon = models.ImageField(
        _('Icon'), upload_to='icons', null=True, blank=True
    )

    class Meta:
        verbose_name = _('specialty')
        verbose_name_plural = _('specialties')

    def __str__(self):
        return self.specialty


class DoctorData(models.Model):
    crm = models.CharField(_('CRM'), max_length=30)
    name = models.CharField(_('Name'), max_length=100)
    zip_code = models.CharField(
        _('Zip Code'),
        max_length=9,
        validators=[cep_validator],
    )
    street = models.CharField(_('Street'), max_length=100)
    neighborhood = models.CharField(_('Neighborhood'), max_length=100)
    number = models.IntegerField(_('Number'))
    rg = models.ImageField(_('RG'), upload_to='rgs')
    digital_crm = models.ImageField(
        _('Digital CRM'),
        upload_to='medical_identifications',
    )
    photo = models.ImageField(_('Photo'), upload_to='profile_photos')
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        verbose_name=_('User'),
    )
    description = models.TextField(_('Description'), null=True, blank=True)
    specialty = models.ForeignKey(
        Specialties,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        verbose_name=_('Specialty'),
    )
    consultation_fee = models.FloatField(_('Consultation Fee'), default=100)

    class Meta:
        verbose_name = _('doctor data')
        verbose_name_plural = _('doctors data')

    def __str__(self):
        return self.user.username

    def next_schedule(self):
        OpenedDate = apps.get_model('doctor', 'OpenedDate')
        return (
            OpenedDate.objects.filter(user=self.user)
            .filter(date__gt=datetime.now())
            .filter(scheduled=False)
            .order_by('date')
            .first()
        )


class OpenedDate(models.Model):
    date = models.DateTimeField(_('date'))
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, verbose_name=_('user')
    )
    scheduled = models.BooleanField(verbose_name=_('scheduled'), default=False)

    def __str__(self):
        return f'{self.date}'

    class Meta:
        verbose_name = _('opened date')
        verbose_name_plural = _('opened dates')
