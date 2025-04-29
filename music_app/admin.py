from django.contrib import admin
from .models import Artist, Album, Category, Song
# from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser

# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     list_display = ('username', 'email', 'is_staff', 'is_active', 'date_joined', 'last_login')
#     list_filter = ('is_staff', 'is_active')
#     fieldsets = (
#         (None, {'fields': ('username', 'email', 'password')}),
#         ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
#         ('Important Dates', {'fields': ('last_login', 'date_joined')}),
#     )
#     search_fields = ('username', 'email')
#     ordering = ('date_joined',)

# admin.site.register(CustomUser, CustomUserAdmin)



@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'release_date')
    list_filter = ('artist', 'release_date')
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album')
    list_filter = ('artist', 'album', 'categories')
    search_fields = ('title',)
