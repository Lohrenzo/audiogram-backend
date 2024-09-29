from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User
from .validators import validate_dob


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    dob = serializers.DateField(required=True)
    image = serializers.ImageField(allow_empty_file=True, required=False)
    is_admin = serializers.BooleanField(default=False, read_only=True)
    is_artist = serializers.BooleanField(default=False, read_only=False)

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "bio",
            "dob",
            "image",
            "is_admin",
            "is_artist",
        )

    def validate_dob(self, value):
        """Validate the Date Of Birth."""
        return validate_dob(value)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        # Capitalize first and last name
        first_name = self.validated_data.get("first_name", "").capitalize()
        last_name = self.validated_data.get("last_name", "").capitalize()
        # Lowercase the email
        email = self.validated_data.get("email", "").lower()
        data.update(
            {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "bio": self.validated_data.get("bio", ""),
                "dob": self.validated_data.get("dob", ""),
                "image": self.validated_data.get("image", None),
                "is_artist": self.validated_data.get(
                    "is_artist", False
                ),  # Ensure default is False
            }
        )
        return data

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data.get("first_name").capitalize()
        user.last_name = self.cleaned_data.get("last_name").capitalize()
        user.email = self.cleaned_data["email"]
        user.bio = self.cleaned_data.get("bio")
        user.dob = self.cleaned_data.get("dob")
        user.is_artist = self.cleaned_data.get(
            "is_artist"
        )  # Update the is_artist attribute

        # Check if an image was uploaded
        if self.cleaned_data.get("image"):
            user.image = self.cleaned_data["image"]

        user.save()
        return user


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    """
    Custom serializer for the User model to include
    additional fields like dob, bio, email, image, etc.
    """

    class Meta:
        model = User
        fields = (
            "pk",  # Primary Key
            "username",  # Username (default field)
            "email",  # Email (readonly)
            "first_name",  # First name (default field)
            "last_name",  # Last name (default field)
            "dob",  # Date of birth (additional field)
            "bio",  # Biography (additional field)
            "image",  # Profile image (additional field)
        )
        # Make email and primary key read-only
        read_only_fields = ("pk", "email")


class UserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    dob = serializers.DateField(required=False)
    image = serializers.ImageField(allow_empty_file=True, required=False)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "bio",
            "dob",
            "image",
        )

    def validate_dob(self, value):
        """Validate the Date Of Birth."""
        return validate_dob(value)

    def update(self, instance, validated_data):
        """Update user details"""

        # Update only the fields that are provided in the request
        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()
        return instance


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        """
        Ensure that the provided old password matches
        the current user's password.
        """
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate_new_password(self, value):
        """
        Validate the new password using Django's built-in password validators.
        You can also add custom password validation here if needed.
        """
        # Use Django's built-in password validators (e.g., length, complexity).
        validate_password(value)
        return value

    def validate(self, data):
        """
        Ensure that the new password is different from the old password.
        """
        old_password = data.get("old_password")
        new_password = data.get("new_password")

        if old_password == new_password:
            raise serializers.ValidationError(
                "The new password cannot be the same as the old password."
            )

        return data

    def save(self, **kwargs):
        """
        Set the new password for the user and save it.
        """
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
