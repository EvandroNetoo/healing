# Generated by Django 5.0.4 on 2024-04-17 17:27

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0007_rename_opendates_openeddates_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OpenedDates',
            new_name='OpenedDate',
        ),
    ]
