from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class UserRegisterSerializer(serializers.ModelSerializer):
    repeat_password = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'password', 'repeat_password', 'tg_username']

    def save(self, request):
        user = User(
            email=self.validated_data['email'],
            first_name=self.validated_data['email'],
            last_name=self.validated_data['email'],
            tg_user_name=self.validated_data['tg_user_name'],
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
