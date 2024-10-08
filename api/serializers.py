# from django.conf.global_settings import AUTH_USER_MODEL
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from authentication.models import User

from .models import Album, Audio, Genre, Playlist


class GenreSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(default="")

    class Meta:
        model = Genre
        fields = "__all__"

    def create(self, validated_data):
        """
        Create and return a new `Genre` instance, given the validated data.
        """
        return Genre.objects.create(**validated_data)

    def validate(self, data):
        """
        Check if the genre title already exists.
        """
        title = data.get("title")
        if Genre.objects.filter(title=title).exists():
            raise serializers.ValidationError(f"{title} already exists!!")
        return data


class AudioSerializer(serializers.ModelSerializer):
    # genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all())
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field="title",
    )
    artist = serializers.SlugRelatedField(
        # queryset=AUTH_USER_MODEL.objects.all(),
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
        slug_field="username",
    )
    title = serializers.CharField(
        required=True,
        max_length=255,
        validators=[
            UniqueValidator(queryset=Audio.objects.all()),
        ],
    )  # Unique Validator for title. 1st Method
    album = serializers.SlugRelatedField(
        queryset=Album.objects.all(),
        slug_field="title",
        required=False,  # Make the album field optional
        allow_null=True,
    )
    audio = serializers.FileField()
    cover = serializers.ImageField(allow_empty_file=True, required=False)
    released = serializers.DateTimeField(read_only=True)
    edited = serializers.DateTimeField(read_only=True)
    play_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Audio
        fields = (
            "id",
            "title",
            "artist",
            "producer",
            "audio",
            "cover",
            "album",
            "status",
            "likes",
            "genre",
            "released",
            "edited",
            "play_count",
        )

    def create(self, validated_data):
        # Check if the audio is properly opened before saving
        if "audio" in validated_data:
            # Ensure that audio is being uploaded
            print("Audio file received: ", validated_data.get("audio"))

            if "album" not in validated_data or not validated_data["album"]:
                # Create a new album if no album is provided
                album_title = f"{validated_data['title']} - Single"
                album_cover = validated_data.get("cover")

                # Ensure the artist is provided in validated_data
                artist = validated_data.get("artist")
                if artist is None:
                    raise serializers.ValidationError(
                        {"artist": "Artist is required to create an album."}
                    )

                album, created = Album.objects.get_or_create(
                    title=album_title,
                    artist=artist,
                    defaults={"cover": album_cover},
                )

                # Optionally log whether the album was created or retrieved
                if created:
                    print(f"Created new album: {album_title}")
                else:
                    print(f"Retrieved existing album: {album_title}")

                validated_data["album"] = album
            # audio = validated_data["audio"]

            # validated_data["audio"] = audio.file
            print("Validated Data For Audio: ", validated_data)

        return super().create(validated_data)


class AlbumSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(default="")
    artist = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
        slug_field="username",
    )
    cover = serializers.ImageField(allow_empty_file=True)
    audios = AudioSerializer(many=True, read_only=True, source="audio_album")
    released = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Album
        fields = (
            "id",
            "title",
            "description",
            "artist",
            "cover",
            "audios",
            "released",
        )

    def create(self, validated_data):
        """
        Create and return a new `Album` instance, given the validated data.
        """
        return Album.objects.create(**validated_data)

    # def create(self, validated_data):
    #     # Use the artist from the request context if not provided
    #     if "artist" not in validated_data:
    #         validated_data["artist"] = self.context["request"].user
    #     return super().create(validated_data)


class PlaylistAudiosField(serializers.ListField):
    def to_representation(self, value):
        # Return full audio objects during serialization (GET requests)
        return AudioSerializer(value, many=True).data

    def to_internal_value(self, data):
        # Accept audio IDs during deserialization (POST requests)
        audio_ids = data
        audios = Audio.objects.filter(pk__in=audio_ids)
        return list(audios)


class PlaylistSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(
        required=False,
        allow_null=True,
        default="",
    )
    creator = serializers.SlugRelatedField(
        # queryset=User.objects.all(),
        slug_field="username",
        default=serializers.CurrentUserDefault(),
        read_only=True,
    )
    audios = PlaylistAudiosField(required=False)
    # audios = AudioSerializer(many=True)
    # audios = serializers.PrimaryKeyRelatedField(
    #     queryset=Audio.objects.all(),
    #     many=True,  # Allow multiple audios
    # )
    created = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Playlist
        fields = (
            "id",
            "title",
            "description",
            "creator",
            "audios",
            "created",
        )

    def create(self, validated_data):
        # Pop the audios field from validated_data if it exists
        audios = validated_data.pop("audios", None)
        playlist = Playlist.objects.create(**validated_data)

        # If audios were provided, add them to the playlist
        if audios:
            playlist.audios.add(*audios)

        return playlist
