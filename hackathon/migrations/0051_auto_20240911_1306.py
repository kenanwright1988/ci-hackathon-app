# Generated by Django 3.1.13 on 2024-09-11 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hackathon', '0050_hackathon_google_registrations_form'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hackathon',
            old_name='google_registrations_form',
            new_name='google_registration_form',
        ),
    ]
