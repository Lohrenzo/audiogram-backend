from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import User


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    dob = serializers.DateField(required=True)
    # image = serializers.ImageField(allow_empty_file=True)
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
            # "image",
            "is_admin",
            "is_artist",
        )

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update(
            {
                "first_name": self.validated_data.get("first_name", ""),
                "last_name": self.validated_data.get("last_name", ""),
                "bio": self.validated_data.get("bio", ""),
                "dob": self.validated_data.get("dob", ""),
                # "image": self.validated_data.get("image", ""),
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
        user.save()
        return user

    #
    # def to_representation(self, instance):
    #     """Customize the representation of the user data."""
    #     representation = super().to_representation(instance)
    #     representation["is_artist"] = instance.is_artist
    #     representation["bio"] = instance.bio
    #     representation["dob"] = instance.dob
    #     representation["image"] = instance.image.url if instance.image else None
    #     return representation
