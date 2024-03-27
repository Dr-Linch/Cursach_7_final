from django.urls import path
from habits.apps import HabitsConfig
from habits import views

app_name = HabitsConfig.name

urlpatterns = [
    path('habits/', views.HabitListAPIView.as_view(), name='habits_list'),
    path('habit/<int:pk>/', views.HabitRetrieveAPIView.as_view(), name='habit_detail'),
    path('habit/create/', views.HabitCreateAPIView.as_view(), name='habit_create'),
    path('habit/update/<int:pk>/', views.HabitUpdateAPIView.as_view(), name='habit_update'),
    path('habit/delete/<int:pk>/', views.HabitDestroyAPIView.as_view(), name='habit_delete'),
    path('habits/public/', views.PublicHabitListView.as_view(), name='public_habits_list')
]
