from django.contrib import admin
from .models import Playlist

# admin.site.register(Playlist)
# admin.site.register(PlaylistForm)
@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)