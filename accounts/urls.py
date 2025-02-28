from django.urls import path

from accounts import views

urlpatterns = [
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('user/update/avatar/', views.EditUserAvatarAPIView.as_view(), name='update_user_avatar'),
    path('user/create/', views.CreateUserAPIView.as_view(), name='update_create'),
    path('user/update/', views.EditUserAPIView.as_view(), name='update_user'),
]
