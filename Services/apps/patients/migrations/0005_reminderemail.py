# Generated by Django 2.0.7 on 2018-10-04 06:44

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0004_patientprofile_emr_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReminderEmail',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('subject', models.CharField(max_length=140)),
                ('message', models.CharField(max_length=500)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.PatientProfile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
