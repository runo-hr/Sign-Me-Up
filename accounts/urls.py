# accounts/urls.py
from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserProfileView, VerifyEmailView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
]
