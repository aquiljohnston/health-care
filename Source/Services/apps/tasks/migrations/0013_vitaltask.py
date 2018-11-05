# Generated by Django 2.0.7 on 2018-09-20 06:27

import apps.tasks.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0005_goalcomment'),
        ('tasks', '0012_vitaltasktemplate'),
    ]

    operations = [
        migrations.CreateModel(
            name='VitalTask',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('appear_datetime', models.DateTimeField()),
                ('due_datetime', models.DateTimeField()),
                ('is_complete', models.BooleanField(default=False, editable=False, help_text='Set to True if all questions has its corresponding response.')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vital_tasks', to='plans.CarePlan')),
                ('vital_task_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vital_tasks', to='tasks.VitalTaskTemplate')),
            ],
            options={
                'ordering': ('appear_datetime',),
            },
            bases=(models.Model, apps.tasks.models.StateMixin),
        ),
    ]
