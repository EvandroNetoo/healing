# Generated by Django 5.0.4 on 2024-04-17 16:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0005_alter_doctordata_zip_code'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='doctordata',
            options={
                'verbose_name': 'doctor data',
                'verbose_name_plural': 'doctors data',
            },
        ),
        migrations.AlterModelOptions(
            name='specialties',
            options={
                'verbose_name': 'specialty',
                'verbose_name_plural': 'specialties',
            },
        ),
        migrations.CreateModel(
            name='OpenDates',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('date', models.DateTimeField(verbose_name='date')),
                (
                    'scheduled',
                    models.BooleanField(
                        default=False, verbose_name='scheduled'
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='user',
                    ),
                ),
            ],
        ),
    ]