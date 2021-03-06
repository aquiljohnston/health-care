# Generated by Django 2.0.7 on 2018-07-23 15:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=140)),
                ('dx_code', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'diagnosis',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='EmployeeProfile',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('npi_code', models.CharField(blank=True, help_text="By adding the NPI number to the user profile, we can link providers to the electronic medical records (EMR). If the user is not a provider they won't have an NPI number.", max_length=100, null=True)),
            ],
            options={
                'ordering': ('user',),
            },
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('addr_street', models.CharField(blank=True, max_length=255, null=True)),
                ('addr_suite', models.CharField(blank=True, max_length=35, null=True)),
                ('addr_city', models.CharField(blank=True, max_length=255, null=True)),
                ('addr_state', models.CharField(blank=True, max_length=255, null=True)),
                ('addr_zip', models.CharField(blank=True, max_length=15, null=True)),
                ('name', models.CharField(max_length=120)),
                ('is_affiliate', models.BooleanField(default=False)),
                ('parent_company', models.CharField(blank=True, max_length=120, null=True)),
            ],
            options={
                'verbose_name_plural': 'facilities',
                'ordering': ('organization', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=140)),
                ('rx_code', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('addr_street', models.CharField(blank=True, max_length=255, null=True)),
                ('addr_suite', models.CharField(blank=True, max_length=35, null=True)),
                ('addr_city', models.CharField(blank=True, max_length=255, null=True)),
                ('addr_state', models.CharField(blank=True, max_length=255, null=True)),
                ('addr_zip', models.CharField(blank=True, max_length=15, null=True)),
                ('name', models.CharField(max_length=120)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Procedure',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=140)),
                ('px_code', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ProviderRole',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=35)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ProviderSpecialty',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=35)),
                ('physician_specialty', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'provider specialties',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ProviderTitle',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=35)),
                ('abbreviation', models.CharField(max_length=10)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='facility',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Organization'),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='facilities',
            field=models.ManyToManyField(blank=True, related_name='employees', to='core.Facility'),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='facilities_managed',
            field=models.ManyToManyField(blank=True, related_name='managers', to='core.Facility'),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='organizations',
            field=models.ManyToManyField(blank=True, related_name='employees', to='core.Organization'),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='organizations_managed',
            field=models.ManyToManyField(blank=True, related_name='managers', to='core.Organization'),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='roles',
            field=models.ManyToManyField(to='core.ProviderRole'),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='specialty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.ProviderSpecialty'),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.ProviderTitle'),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
