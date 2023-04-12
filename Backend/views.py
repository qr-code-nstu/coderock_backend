from django.contrib.auth import login, logout
from django.shortcuts import render
from django.views import View
from rest_framework import permissions, status
from rest_framework.response import Response

from .models import *
from .serializers import *
from rest_framework.generics import *


class MainView(ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class UserSignIn(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSignInSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)


class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        logout(request)
        return Response('User Logged out successfully')
