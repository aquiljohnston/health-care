# Generated by Django 2.0.7 on 2019-02-28 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0021_merge_20190225_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='problemarea',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
