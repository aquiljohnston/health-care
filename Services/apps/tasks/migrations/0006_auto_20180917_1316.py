# Generated by Django 2.0.7 on 2018-09-17 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_teamtask_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assessmentresponse',
            options={'ordering': ('assessment_task__appear_datetime',)},
        ),
        migrations.AlterModelOptions(
            name='assessmenttask',
            options={'ordering': ('appear_datetime',)},
        ),
        migrations.AlterModelOptions(
            name='medicationtask',
            options={'ordering': ('appear_datetime',)},
        ),
        migrations.AlterModelOptions(
            name='symptomtask',
            options={'ordering': ('appear_datetime',)},
        ),
    ]
