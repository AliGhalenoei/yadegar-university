from django.urls import path 
from rest_framework_simplejwt.views import TokenRefreshView
from .import views

urlpatterns = [
    path("login/",views.UserLoginAPIView.as_view()),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("logout/",views.UserLogoutAPIView.as_view()),
    path("register/",views.UserRegisterAPIView.as_view()),
    path("register/verify/",views.UserRegisterVerifyAPIView.as_view()),
    path("register/complete/",views.UserRegisterCompleteAPIView.as_view()),
]
