from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['email']
        fields = '__all__'

class UserRegisterSerializer(serializers.ModelSerializer):
    repeat_password = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['email', 'password', 'repeat_password', 'tg_username']

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['email'],
            last_name=validated_data['email'],
            tg_username=validated_data['tg_username'],
            is_superuser=False,
            is_staff=False,
            is_active=True
        )

        password = self.validated_data['password']
        repeat_password = self.validated_data['repeat_password']
        if password != repeat_password:
            raise serializers.ValidationError('Пароли не совпадают')
        user.set_password(password)
        user.save()
        return user
