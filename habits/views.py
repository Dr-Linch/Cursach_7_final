from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.serializers import HabitSerializer
from users.permissions import IsOwner


class HabitListAPIView(generics.ListAPIView):
    """
    Список всех привычек
    """
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = HabitSerializer

    def get_queryset(self):
        user = self.request.user
        owners_list = []
        owners = Habit.objects.filter()
        for owner in owners:
            if owner.is_public is True:
                owners_list.append(owner)
            else:
                if owner.owner == user:
                    owners_list.append(owner)
        return owners_list


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """
    Детализация привычки
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class HabitCreateAPIView(generics.CreateAPIView):
    """
    Создание новой привычки
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        new_habit = serializer.save()
        new_habit.owner = self.request.user
        new_habit.save()


class HabitUpdateAPIView(generics.UpdateAPIView):
    """
    Редактирование привычки
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class HabitDestroyAPIView(generics.DestroyAPIView):
    """
    Удалние привычки
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class PublicHabitListView(generics.ListAPIView):
    """
    Список привычек общего доступа
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    def get_queryset(self):
        owners = Habit.objects.filter(is_public=True)
        return owners
