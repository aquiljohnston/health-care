# Generated by Django 2.0.7 on 2019-04-26 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0048_careplanassessmenttemplate'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessmenttask',
            name='assessment_template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tasks.CarePlanAssessmentTemplate'),
        ),
    ]
