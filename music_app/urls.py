from django.urls import path
from music_app.views import add_album, add_artist, add_category, home, login_view, logout_view, signup_view, song_list, upload_song, artist_detail, category_detail
urlpatterns = [
    path('home/', home, name='home'),
    path('', song_list, name='song_list'),
    path('upload_song/', upload_song, name='upload_song'),
    path('add-artist/', add_artist, name='add_artist'),
    path('add-album/', add_album, name='add_album'),
    path('add-category/', add_category, name='add_category'),
    path('signup/', signup_view, name='signup'),
    path('artist/<int:artist_id>/', artist_detail, name='artist_detail'),
    path('category/<int:category_id>/', category_detail, name='category_detail'),
    # path('login/', login_view, name='login'),
    # path('logout/', logout_view, name='logout'),
    # path('user-activity/', user_activity_view, name='user_activity'),
]
