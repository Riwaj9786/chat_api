from django.urls import path

from chat import views

urlpatterns = [
    path('room/detail/<str:slug>/', views.ChatRoomAPIView.as_view(), name='get_room'),
    path('room/create/', views.CreateChatRoomAPIView.as_view(), name='room_create'),
    path('room/<str:slug>/members/add/', views.AddUserToChatRoomAPIView.as_view(), name='add_room_members'),
]
