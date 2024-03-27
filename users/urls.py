from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.apps import UsersConfig
from users import views

app_name = UsersConfig.name

urlpatterns = [
    path('', views.UserListAPIView.as_view(), name='user_list'),
    path('create/', views.UserCreateAPIView.as_view(), name='user_create'),
    path('<int:pk>/', views.UserDetailAPIView.as_view(), name='user_detail'),
    path('update/<int:pk>/', views.UserUpdateAPIView.as_view(), name='user_update'),
    path('delete/<int:pk>/', views.UserDestroyAPIView.as_view(), name='user_delete'),
    path('register/', views.UserRegisterAPIView.as_view(), name='user_register'),

    path('token/', TokenObtainPairView.as_view(), name='token_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
