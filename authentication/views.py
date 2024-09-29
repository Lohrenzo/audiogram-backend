from dj_rest_auth.registration.views import SocialLoginView, RegisterView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.views import LoginView, UserDetailsView
from .serializers import (
    CustomRegisterSerializer,
    PasswordChangeSerializer,
    UserUpdateSerializer,
    CustomUserDetailsSerializer,
)
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser

# from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer
    parser_classes = [MultiPartParser, JSONParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = self.get_response_data(user)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    # def get_response_data(self, user):
    #     # Generate the tokens for the user
    #     refresh = RefreshToken.for_user(user)
    #     access = refresh.access_token

    #     # Custom response data
    #     data = {
    #         "access": str(access),
    #         "refresh": str(refresh),
    #         "user": {
    #             "pk": user.pk,
    #             "username": user.username,
    #             "email": user.email,
    #             "first_name": user.first_name,
    #             "last_name": user.last_name,
    #             "is_artist": user.is_artist,
    #             "bio": user.bio,
    #             "dob": user.dob,
    #             "image": user.image.url if user.image else None,
    #         },
    #     }
    #     return data


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

        return Response(custom_response)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://127.0.0.1:3000/"
    client_class = OAuth2Client


class CustomUserDetailsView(UserDetailsView):
    serializer_class = CustomUserDetailsSerializer


class UserUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, JSONParser]

    def get_object(self):
        # Return the current authenticated user
        return self.request.user


class PasswordChangeView(generics.UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def get_object(self):
        # Return the current authenticated user
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Password updated successfully."},
            status=status.HTTP_200_OK,
        )
