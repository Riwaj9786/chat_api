from django.contrib.auth import login

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from accounts.models import User
from accounts.serializers import (
    EditUserAvatarSerializer,
    EditUserSerializer,
    LoginSerializer,
    CreateUserSerializer,
    )

from knox import views as knox_views

class LoginAPIView(knox_views.LoginView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)
            response = super().post(request, format=None)
            print(type(response.data['token']))
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            response.data,
            status=status.HTTP_200_OK
        )

class EditUserAvatarAPIView(generics.UpdateAPIView):
    serializer_class = EditUserAvatarSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_object(self):
        return self.request.user

class EditUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        serializer = EditUserSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(partial=True)
            return Response(
                {
                    'message': "User updated successfully!",
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateUserAPIView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)        