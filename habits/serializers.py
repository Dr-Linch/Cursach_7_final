from rest_framework import serializers
from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        habit = Habit.objects.create(**validated_data)

        if habit.duration > 120:
            raise serializers.ValidationError("Продолжиьельность больше 120 минут")

        if not habit.is_pleasant:
            if not habit.tribute:
                if not habit.pleasant_link:
                    raise serializers.ValidationError("Обычная привычка должна иметь награду или быть приятной")
            else:
                if habit.pleasant_link:
                    raise serializers.ValidationError("Обычная привычка не может одновременно"
                                                      " иметь награду и быть приятной")
        else:
            if habit.tribute:
                raise serializers.ValidationError("Приятная привычка не вознаграждается")
        return habit

    class Meta:
        model = Habit
        fields = '__all__'
