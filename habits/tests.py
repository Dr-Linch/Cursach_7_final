from django.test import TestCase
from rest_framework import status
from habits.models import Habit
from users.models import User
from rest_framework.test import APIClient
from django.urls import reverse


class HabitsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@hell.aid',
            first_name='Mihalych',
            is_superuser=False,
            is_staff=False,
            is_active=True
        )
        self.user.set_password('666')
        self.user.save()

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_habit_create(self):
        """
        Тестовое создание привычки
        """
        data = {
            'place': 'Тир',
            'time': '18:00:00',
            'action': 'Стрелять по мишеням',
            'is_pleasant': False,
            'frequency': 'Saturday',
            'tribute': 'запах пороха, повышение навыка',
            'duration': 20,
            'is_public': True,
            'owner': self.user.pk
        }

        response = self.client.post(
            reverse('habits:habit_create'),
            kwargs={'pk': self.user.pk},
            data=data
        )
        print(response.json())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Habit.objects.all().exists())

    def test_get_public_habits(self):
        """
        тест получения публичных привычек
        """
        data_a = {
            'place': 'Улица',
            'time': '08:00:00',
            'action': 'пробежка',
            'is_pleasant': False,
            'frequency': 'Sunday',
            'tribute': 'Стакан молока и печенька',
            'duration': 40,
            'is_public': True,
            'owner': self.user.pk
        }

        data_b = {
            'place': 'Библиотека',
            'time': '15:00:00',
            'action': 'Читать книгу',
            'is_pleasant': False,
            'frequency': 'Saturday',
            'tribute': 'Лечь спать пораньше',
            'duration': 120,
            'is_public': True,
            'owner': self.user.pk
        }
        self.client.post(
            reverse('habits:habit_create'),
            kwargs={'pk': self.user.pk},
            data=data_a
        )
        self.client.post(
            reverse('habits:habit_create'),
            kwargs={'pk': self.user.pk},
            data=data_b
        )
        response = self.client.get(reverse('habits:public_habits_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_validate_duration_create_habit(self):
        """ Тест на создание привычки с продолжительностью более 120 секунд """
        data = {
            "place": "На стадионе",
            "time": "14:00:00",
            "action": "Пробежать 5 км",
            "is_pleasant": False,
            "frequency": "Sunday",
            "tribute": "Попить виски с колой",
            "duration": 2000,
            "is_public": True,
            "owner": self.user.pk
        }

        response = self.client.post(
            reverse("habits:habit_create"),
            kwargs={'pk': self.user.pk},
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validate_pleasant_create_habit(self):
        """ Тест на создание приятной привычки с наградой """
        data = {
            "place": "Дома",
            "time": "20:00:00",
            "action": "Расслабиться под звуки природы",
            "is_pleasant": True,
            "frequency": "Monday",
            "tribute": "Съесть сладкий рулет",
            "duration": 120,
            "is_public": False,
            "owner": self.user.pk
        }

        response = self.client.post(
            reverse("habits:habit_create"),
            kwargs={'pk': self.user.pk},
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validate_usual_create_habit(self):
        """ Тест на создание обычной привычки без награды """
        data = {
            "place": "В лесу",
            "time": "14:00:00",
            "action": "Поскримить",
            "is_pleasant": False,
            "frequency": "Friday",
            "duration": 60,
            "is_public": True,
            "owner": self.user.pk
        }

        response = self.client.post(
            reverse("habits:habit_create"),
            kwargs={'pk': self.user.pk},
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
