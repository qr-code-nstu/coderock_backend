from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('main/', MainView.as_view()),
    path('user/signin/', UserSignIn.as_view()),
    path('user/logout/', LogoutView.as_view()),
    path('user/login/', ApiToken.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('client/signin/', ClientSignIn.as_view()),
    path('executor/signin/', ExecutorSignIn.as_view()),
    path('categories/', CategoriesView.as_view()),
    path('isi/', IsI.as_view()),
]
