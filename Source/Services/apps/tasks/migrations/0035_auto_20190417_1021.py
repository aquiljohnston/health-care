# Generated by Django 2.0.7 on 2019-04-17 16:21

from django.db import migrations


def assign_plan_templates(apps, schema_editor):
    """
    This function will iterate over all :model:`tasks.PatientTask`
    and do the following on each instance:

    - create CarePlanPatientTemplate object based on plan and
        patient_task_template
    - assign the created CarePlanPatientTemplate object above into the
        patient_template field
    """
    PatientTask = apps.get_model('tasks', 'PatientTask')
    CarePlanPatientTemplate = apps.get_model('tasks',
                                             'CarePlanPatientTemplate')
    for task in PatientTask.objects.all():
        patient_template = CarePlanPatientTemplate.objects.create(
            plan=task.plan,
            patient_task_template=task.patient_task_template
        )

        task.patient_template = patient_template
        task.save(update_fields=['[patient_template'])


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0034_auto_20190417_1021'),
    ]

    operations = [
        migrations.RunPython(assign_plan_templates)
    ]