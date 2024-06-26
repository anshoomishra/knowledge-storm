# Generated by Django 4.2 on 2024-07-01 04:47

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0003_testattempt_questionattempt'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testattempt',
            old_name='completed_at',
            new_name='end_time',
        ),
        migrations.RenameField(
            model_name='testattempt',
            old_name='started_at',
            new_name='start_time',
        ),
        migrations.RemoveField(
            model_name='testattempt',
            name='total_time_spent',
        ),
        migrations.AddField(
            model_name='testattempt',
            name='current_question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='current_attempts', to='exam.question'),
        ),
        migrations.AddField(
            model_name='testattempt',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='testattempt',
            name='paused_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='testattempt',
            name='time_spent',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
        migrations.AlterField(
            model_name='testattempt',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_attempts', to='exam.test'),
        ),
    ]
