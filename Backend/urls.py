from django.urls import path
from .views import *

urlpatterns = [
    path('main/', MainView.as_view()),
    path('user/signin/', UserSignIn.as_view()),
    path('user/login/', LoginView.as_view()),
    path('user/logout/', LogoutView.as_view()),
]
