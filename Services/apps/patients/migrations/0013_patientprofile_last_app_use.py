# Generated by Django 2.0.7 on 2018-10-23 02:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0012_auto_20181018_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientprofile',
            name='last_app_use',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
