from dj_rest_auth.jwt_auth import get_refresh_view

# from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LogoutView  # LoginView
from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView, TokenBlacklistView

# from allauth.socialaccount.views import signup
from .views import (
    # GoogleLogin,
    CustomRegisterView,
    CustomLoginView,
    UserUpdateView,
    PasswordChangeView,
    CustomUserDetailsView,
)


urlpatterns = [
    path("register/", CustomRegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("user/", CustomUserDetailsView.as_view(), name="user_details"),
    path("user/update/", UserUpdateView.as_view(), name="user_update"),
    path(
        "user/change-password/",
        PasswordChangeView.as_view(),
        name="change_password",
    ),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("token/refresh/", get_refresh_view().as_view(), name="token_refresh"),
    path(
        "token/blacklist",
        TokenBlacklistView.as_view(),
        name="token_blacklist",
    ),
    # path("google/", GoogleLogin.as_view(), name="google_login"),
]
