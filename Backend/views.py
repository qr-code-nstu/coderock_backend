from django.shortcuts import render
from django.views import View
from .models import *
from .serializers import *
from rest_framework.generics import *


class MainView(ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class UserSignIn(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignInSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



# Create your views here.
