# from django.shortcuts import render
from dj_rest_auth.registration.views import SocialLoginView, RegisterView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.views import LoginView
from .serializers import CustomRegisterSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    def get_response_data(self, user):
        # Generate the tokens for the user
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        # Custom response data
        data = {
            "access": str(access),
            "refresh": str(refresh),
            "user": {
                "pk": user.pk,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_artist": user.is_artist,
                "bio": user.bio,
                "dob": user.dob,
                "image": user.image.url if user.image else None,
            },
        }
        return data


class CustomLoginView(LoginView):
    def get_response(self):
        # Get the original response data
        original_response = super().get_response().data

        # Add custom fields to the response data
        user_data = {
            "id": self.user.pk,
            "username": self.user.username,
            "email": self.user.email,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "is_artist": self.user.is_artist,
            "bio": self.user.bio,
            "dob": self.user.dob,
            "image": self.user.image.url if self.user.image else None,
        }

        # Construct the custom response structure
        custom_response = {
            # Unpack user_data dictionary into the custom_response dictionary
            **user_data,
            "access": original_response.get("access"),
            "refresh": original_response.get("refresh"),
        }

        # custom_response = user_data

        return Response(custom_response)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://127.0.0.1:3000/"
    client_class = OAuth2Client
