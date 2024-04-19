from django.utils.translation import gettext_lazy as _
from django.db import models

from accounts.models import User
from doctor.models import OpenedDate


class Appointment(models.Model):
    status_choices = (
        ('A', _('Scheduled')),
        ('F', _('Finished')),
        ('C', _('Cancelled')),
        ('I', _('Started')),
    )
    patient = models.ForeignKey(
        User, verbose_name=_('patient'), on_delete=models.DO_NOTHING
    )
    opened_date = models.ForeignKey(
        OpenedDate, on_delete=models.DO_NOTHING, verbose_name=_('opened_date')
    )
    status = models.CharField(
        verbose_name=_('status'),
        max_length=1,
        choices=status_choices,
        default='A',
    )
    link = models.URLField(verbose_name=_('link'), null=True, blank=True)

    class Meta:
        verbose_name = _('appointment')
        verbose_name_plural = _('appointments')

    def __str__(self):
        return self.patient.username


class Document(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.DO_NOTHING, verbose_name=_('appointment'))
    title = models.CharField(max_length=30, verbose_name=_('title'))
    document = models.FileField(upload_to='documents', verbose_name=_('document'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('document')
        verbose_name_plural = _('documents')