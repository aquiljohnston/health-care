# Generated by Django 2.0.7 on 2018-09-19 05:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('plans', '0004_goalprogress'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoalComment',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='plans.Goal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goal_comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Goal Comment',
                'verbose_name_plural': 'Goal Comments',
            },
        ),
    ]
