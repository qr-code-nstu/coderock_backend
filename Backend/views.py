from django.contrib.auth import login, logout
from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import Group
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .models import *
from .serializers import *
from rest_framework.generics import *


class MainView(ListAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class IsI(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    authentication_class = JWTTokenUserAuthentication

    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        try:
            valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
            user_id = valid_data['user_id']
            request.user = User.objects.get(id=user_id)
        except ValidationError as v:
            print("validation error", v)
        user = request.user
        g1 = Group.objects.get(name='Executor')
        g2 = Group.objects.get(name='Client')
        g11 = user.groups.filter(name=g1.name).exists()
        g22 = user.groups.filter(name=g2.name).exists()
        if g11:
            return Response(data={'you': g1.name}, status=status.HTTP_200_OK)

        elif g22:
            return Response(data={'you': g2.name}, status=status.HTTP_200_OK)
        else:
            return Response(data={'you': 'No'}, status=status.HTTP_200_OK)


class ApiToken(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    authentication_class = None

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = serializer.validated_data

        user = User.objects.get(username=request.data['username'])
        try:
            g1 = Group.objects.get(name='Client')
        except Group.DoewNotExists:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

        try:
            g2 = Group.objects.get(name='Executor')
        except Group.DoewNotExists:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

        if self.request.data['client']:
            is_client = Client.objects.filter(id=user).exists()
            if is_client:
                response['client'] = True
            else:
                response['client'] = False
            try:
                g1.user_set.add(user)
                g2.user_set.remove(user)
            except BaseException:
                return Response(data={'err': '1'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            is_executor = Executor.objects.filter(id=user).exists()
            if is_executor:
                response['executor'] = True
            else:
                response['executor'] = False
            try:
                g2.user_set.add(user)
                g1.user_set.remove(user)
            except BaseException:
                return Response(data={'err': '2'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(response, status=status.HTTP_202_ACCEPTED)


class CategoriesView(ListAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class UserSignIn(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSignInSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        logout(request)
        return Response('User Logged out successfully')


class ClientSignIn(CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = JWTTokenUserAuthentication
    queryset = Client.objects.all()
    serializer_class = ClientSignInSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        try:
            valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
            user_id = valid_data['user_id']
            request.user = User.objects.get(id=user_id)
        except ValidationError as v:
            print("validation error", v)
        is_client = Client.objects.filter(id=request.user).exists()
        if is_client:
            return Response(data={'err': 'Повторное создание1'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            request.data['id'] = request.user.id
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ExecutorSignIn(CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = JWTTokenUserAuthentication
    queryset = Executor.objects.all()
    serializer_class = ExecutorSignInSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        try:
            valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
            user_id = valid_data['user_id']
            request.user = User.objects.get(id=user_id)
        except ValidationError as v:
            print("validation error", v)
        is_executor = Executor.objects.filter(id=request.user).exists()
        if is_executor:
            return Response(data={'err': 'Повторное создание2'}, status=status.HTTP_400_BAD_REQUEST)
        else:

            request.data['id'] = request.user.id
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)