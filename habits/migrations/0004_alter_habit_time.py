# Generated by Django 5.0.3 on 2024-03-30 09:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0003_alter_habit_frequency_alter_habit_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='time',
            field=models.TimeField(default=datetime.time(9, 13, 2, 743416), verbose_name='Время старта привычки'),
        ),
    ]
