from dj_rest_auth.jwt_auth import get_refresh_view

# from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LogoutView, UserDetailsView  # LoginView
from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView, TokenBlacklistView

# from allauth.socialaccount.views import signup
from .views import GoogleLogin, CustomRegisterView, CustomLoginView


urlpatterns = [
    path("register/", CustomRegisterView.as_view(), name="rest_register"),
    path("login/", CustomLoginView.as_view(), name="rest_login"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path("user/", UserDetailsView.as_view(), name="rest_user_details"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("token/refresh/", get_refresh_view().as_view(), name="token_refresh"),
    path(
        "token/blacklist",
        TokenBlacklistView.as_view(),
        name="token_blacklist",
    ),
    #
    path("google/", GoogleLogin.as_view(), name="google_login"),
]
