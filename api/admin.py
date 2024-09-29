from django.contrib import admin
from .models import Album, Audio, Genre, Playlist


admin.site.register(Album)
admin.site.register(Audio)
admin.site.register(Genre)
admin.site.register(Playlist)
