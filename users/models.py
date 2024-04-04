from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    chat_id = models.BigIntegerField(unique=True, verbose_name='Идентификатор чата', **NULLABLE)
    tg_username = models.CharField(max_length=150, unique=True, verbose_name='Имя пользователя в Telegram')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
