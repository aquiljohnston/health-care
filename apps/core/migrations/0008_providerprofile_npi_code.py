# Generated by Django 2.0.7 on 2018-07-10 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20180709_0245'),
    ]

    operations = [
        migrations.AddField(
            model_name='providerprofile',
            name='npi_code',
            field=models.CharField(blank=True, help_text="By adding the NPI number to the user profile, we can linkproviders to the electronic medical records (EMR). If the user isnot a provider they won't have an NPI number.", max_length=100, null=True),
        ),
    ]
