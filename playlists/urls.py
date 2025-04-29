from django.urls import path

from .views import albums_view, artists_view, charts_view, downloaded_view, events_view, favorites_view, for_you_view, like_song, liked_songs_view, new_releases_view, playlists_view, podcasts_view, profile_view, user_login, user_logout, user_signup
from .views import create_playlist, playlist_detail,user_playlists,library_view,add_to_playlist,search_list,add_song_to_playlist
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('create/', create_playlist, name='create_playlist'),
    # path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('library/', library_view, name='library'),
    path('liked-songs/', liked_songs_view, name='liked_songs'),
    path('like-song/', like_song, name='like_song'),
    path('library/playlists/', playlists_view, name='library_playlists'),
    path('library/podcasts/', podcasts_view, name='library_podcasts'),
    path('library/artists/', artists_view, name='library_artists'),
    path('library/albums/', albums_view, name='library_albums'),
    path('library/favorites/', favorites_view, name='library_favorites'),
    path('library/downloaded/', downloaded_view, name='library_downloaded'),
    path('search/', search_list, name='search_songs'),
    path('', user_playlists, name='user_playlists'),
    path('add-to-playlist/', add_to_playlist, name='add_to_playlist'),
    path('playlist/<int:playlist_id>/', playlist_detail, name='playlist_detail'),  # Playlist detail page
    path('add-song-to-playlist/', add_song_to_playlist, name='add_song_to_playlist'),
      # New category pages
    path('new-releases/', new_releases_view, name='new_releases'),
    path('events/', events_view, name='events'),
    path('charts/', charts_view, name='charts'),
    path('for-you/', for_you_view, name='for_you'),


    path('accounts/signup/',user_signup, name='signup'),
    path('accounts/login/', user_login, name='login'),
    path('accounts/logout/', user_logout, name='logout'),
    path('accounts/profile/', profile_view, name='profile'),
]

