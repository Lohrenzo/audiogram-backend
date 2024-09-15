from dj_rest_auth.registration.serializers import RegisterSerializer
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
        data.update(
            {
                "first_name": self.validated_data.get("first_name", ""),
                "last_name": self.validated_data.get("last_name", ""),
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
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
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


class UserUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    dob = serializers.DateField(required=False)
    image = serializers.ImageField(allow_empty_file=True, required=False)

    class Meta:
        model = User
        fields = (
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
        # Update user details
        # if "first_name" in validated_data:
        #     instance.first_name = validated_data.get(
        #         "first_name",
        #         instance.first_name,
        #     )
        # if "last_name" in validated_data:
        #     instance.last_name = validated_data.get(
        #         "last_name",
        #         instance.last_name,
        #     )
        # if "bio" in validated_data:
        #     instance.bio = validated_data.get("bio", instance.bio)
        # if "dob" in validated_data:
        #     instance.dob = validated_data.get("dob", instance.dob)
        # if "image" in validated_data:
        #     instance.image = validated_data.get("image", instance.image)

        # Update only the fields that are provided in the request
        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()
        return instance


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct.")
        return value

    def validate_new_password(self, value):
        # Optional: Add any custom password validation here if necessary
        return value

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
