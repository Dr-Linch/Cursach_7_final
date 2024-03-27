from django.db import models
from config.settings import AUTH_USER_MODEL
from django.utils import timezone

NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):
    """
    Habit Model
    """
    class HabitFrequency(models.TextChoices):
        Daily = 'D', 'Daily'
        monday = 'M', 'Monday'
        tuesday = 'T', 'Tuesday'
        wednesday = 'W', 'Wednesday'
        thursday = 'TH', 'Thursday'
        friday = 'FR', 'Friday'
        saturday = 'SAT', 'Saturday'
        sunday = 'SUN', 'Sunday'

    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)
    place = models.CharField(max_length=200, verbose_name='Место привычки')
    time = models.TimeField(verbose_name='Время старта привычки', default=timezone.now().time())
    action = models.CharField(max_length=120, verbose_name='Действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='Приятная привычка')
    pleasant_link = models.ForeignKey('self', on_delete=models.CASCADE,
                                      verbose_name='Ссылка на приятную привычку', **NULLABLE)
    frequency = models.CharField(choices=HabitFrequency.choices, default=HabitFrequency.Daily, verbose_name='Частота')
    tribute = models.CharField(max_length=100, verbose_name='Награда', **NULLABLE)
    duration = models.IntegerField(verbose_name='Продолжительность')
    is_public = models.BooleanField(default=True, verbose_name='Публичность')

    def __str__(self):
        return f'Действие: {self.action}\nМесто: {self.place}'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
