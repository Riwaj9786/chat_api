from django.shortcuts import render

from chat.models import ChatRoom
from chat.serializers import (
    CreateChatRoomSerializer,
    ChatRoomSerializer,
    UpdateChatRoomMemberSerializer,
)

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class ChatRoomAPIView(generics.GenericAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, slug, *args, **kwargs):
        user = request.user

        try:
            room = ChatRoom.objects.get(slug=slug)
        except ChatRoom.DoesNotExist:
            return Response(
                {'error': "Chat Room doesn't exist!"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if user in room.members.all():
            serializer = ChatRoomSerializer(room)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': "You are not authorized to view the chatroom."},
                status=status.HTTP_403_FORBIDDEN
            )


class CreateChatRoomAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateChatRoomSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': "Chat Room Created!"},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class AddUserToChatRoomAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateChatRoomMemberSerializer

    def patch(self, request, slug, *args, **kwargs):
        try:
            chat_room = ChatRoom.objects.get(slug=slug)
        except ChatRoom.DoesNotExist:
            return Response(
                {'error': "Chat Room doesn't exist!"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.serializer_class(chat_room, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': "Users added successfully!"},
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)