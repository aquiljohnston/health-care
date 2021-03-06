# Generated by Django 2.0.7 on 2018-10-05 01:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0009_auto_20180927_0139'),
        ('patients', '0005_auto_20181003_2138'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='patientverificationcode',
            options={'ordering': ('-created',), 'verbose_name': 'Patient Verification Code', 'verbose_name_plural': 'Patient Verification Codes'},
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='message_for_day',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patients', to='plans.InfoMessage'),
        ),
    ]
