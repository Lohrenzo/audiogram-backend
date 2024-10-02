from rest_framework import serializers
from .models import StreamRecord
from authentication.models import User


class StreamRecordSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
        slug_field="id",
    )

    class Meta:
        model = StreamRecord
        fields = "__all__"
