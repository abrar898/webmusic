from django.shortcuts import get_object_or_404, render, redirect
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from music_app.models import Album, Artist, Category, Song
from .models import Playlist, UserProfile
from .search_utils import search_songs
from django.db.models import Q
from .forms import PlaylistForm, UserRegistrationForm, UserLoginForm

def create_playlist(request):
    if request.method == "POST":
        playlist_name = request.POST.get("playlist_name")
        selected_songs = request.POST.getlist("selected_songs")
        
        if playlist_name:
            # Create the playlist
            try:
                # Check if user is authenticated
                if request.user.is_authenticated:
                    playlist = Playlist.objects.create(
                        name=playlist_name,
                        user=request.user
                    )
                else:
                    # For anonymous users, create a playlist with a default user or handle differently
                    from django.contrib.auth.models import User
                    default_user = User.objects.first()  # Get the first user as default
                    if default_user:
                        playlist = Playlist.objects.create(
                            name=playlist_name,
                            user=default_user
                        )
                    else:
                        # If no users exist, redirect with an error message
                        return render(request, "create_playlist.html", {
                            "songs": Song.objects.all(),
                            "playlists": Playlist.objects.all(),
                            "error": "Failed to create playlist. Please log in first."
                        })
                
                # Add selected songs to the playlist
                if selected_songs:
                    songs = Song.objects.filter(id__in=selected_songs)
                    playlist.songs.add(*songs)
                
                return redirect('playlist_detail', playlist_id=playlist.id)
            except Exception as e:
                # Handle errors gracefully
                return render(request, "create_playlist.html", {
                    "songs": Song.objects.all(),
                    "playlists": Playlist.objects.all(),
                    "error": f"Failed to create playlist: {str(e)}"
                })
    
    # For GET request, show the song selection interface
    songs = Song.objects.all()
    playlists = Playlist.objects.all()
    
    return render(request, "create_playlist.html", {"songs": songs, "playlists": playlists})

def add_to_playlist(request):
    if request.method == "POST":
        data = json.loads(request.body)
        playlist = get_object_or_404(Playlist, id=data["playlist_id"])
        songs = Song.objects.filter(id__in=data["songs"])
        
        playlist.songs.add(*songs)
        return JsonResponse({"message": "Songs added successfully!"})

    return JsonResponse({"error": "Invalid request"}, status=400)



def playlist_detail(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)  # Fetch user's playlist
    songs = playlist.songs.all()  # Get all songs in the playlist
    context = {
        'playlist': playlist,
        'songs': songs,
        'playlists': Playlist.objects.all(),  # Add all playlists for sidebar
        'categories': Category.objects.all(),  # Keep categories for the sidebar
    }
    return render(request, 'playlist_detail.html', context)

def user_playlists(request):
    search_query = request.GET.get('search', '')
    
    if search_query:
        # Search in song title, artist name, and album name
        songs = Song.objects.filter(
            Q(title__icontains=search_query) 
            # Q(artist__icontains=search_query) | 
            # Q(album__icontains=search_query)
        )
    else:
        songs = Song.objects.all()
    context = {
        'songs': Song.objects.all(),
        'playlists': Playlist.objects.all(),
        'categories': Category.objects.all(),
        'artists': Artist.objects.all(),
    }
    return render(request, 'song_list.html', context)

# @login_required(login_url='song_list')
def liked_songs_view(request):
    if request.user.is_authenticated:
        liked_songs = Song.objects.filter(likes=request.user)
        playlists = Playlist.objects.filter(user=request.user)
    else:
        liked_songs = Song.objects.none()  # Empty queryset for anonymous users
        playlists = Playlist.objects.all()  # Show all playlists for anonymous users
    
    context = {
        'songs': liked_songs,
        'playlists': playlists,
        'categories': Category.objects.all(),
        'page_title': 'Liked Songs',
    }
    return render(request, 'liked_songs.html', context)

# @login_required(login_url='login') 
def library_view(request):
    context = {
        'playlists': Playlist.objects.all(),  # Show all playlists to all users
        'artists': Artist.objects.all(),
        'albums': Album.objects.all(),
        'songs': Song.objects.all(),
        'categories': Category.objects.all(),  # Keep categories for the sidebar
    }
    return render(request, 'library.html', context)

# @login_required(login_url='login')
def playlists_view(request):
    context = {
        'playlists': Playlist.objects.filter(user=request.user),
        'categories': Category.objects.all(),
        'active_tab': 'playlists',
    }
    return render(request, 'library_playlists.html', context)

# @login_required(login_url='login')
def podcasts_view(request):
    # Assuming podcasts are a type of content, filter songs that are podcasts
    # This is a placeholder - modify according to your actual data model
    podcasts = Song.objects.filter(categories__name='Podcast')
    context = {
        'podcasts': podcasts,
        'categories': Category.objects.all(),
        'active_tab': 'podcasts',
    }
    return render(request, 'library_podcasts.html', context)

# @login_required(login_url='login')
def artists_view(request):
    context = {
        'artists': Artist.objects.all(),
        'categories': Category.objects.all(),
        'active_tab': 'artists',
    }
    return render(request, 'library_artists.html', context)

# @login_required(login_url='login')
def albums_view(request):
    context = {
        'albums': Album.objects.all(),
        'categories': Category.objects.all(),
        'active_tab': 'albums',
    }
    return render(request, 'library_albums.html', context)

@login_required(login_url='song_list')
def favorites_view(request):
    # Assuming songs can be liked by users
    liked_songs = Song.objects.filter(likes=request.user)
    context = {
        'songs': liked_songs,
        'categories': Category.objects.all(),
        'active_tab': 'favorites',
    }
    return render(request, 'library_favorites.html', context)

@login_required(login_url='song_list')
def downloaded_view(request):
    # This is a placeholder - implement based on your downloaded content tracking
    # For example, if you have a Downloaded model or field
    downloaded_songs = Song.objects.filter(downloaded_by=request.user)
    context = {
        'songs': downloaded_songs,
        'categories': Category.objects.all(),
        'active_tab': 'downloaded',
    }
    return render(request, 'library_downloaded.html', context)


def search_list(request):
    search_query = request.GET.get('search', '')
    songs = search_songs(search_query)  # Call the search function

    context = {
        'songs': songs,
        'playlists': Playlist.objects.all(),
        'categories': Category.objects.all(),
    }

    return render(request, 'index.html', context)


def add_song_to_playlist(request):
    if request.method == "POST":
        playlist_id = request.POST.get("playlist_id")
        selected_songs = request.POST.getlist("selected_songs")
        
        if not playlist_id or not selected_songs:
            return render(request, "create_playlist.html", {
                "songs": Song.objects.all(),
                "playlists": Playlist.objects.all(),
                "error": "Please select a playlist and at least one song"
            })
        
        try:
            playlist = get_object_or_404(Playlist, id=playlist_id)
            songs = Song.objects.filter(id__in=selected_songs)
            
            playlist.songs.add(*songs)
            return redirect('playlist_detail', playlist_id=playlist.id)
        except Exception as e:
            return render(request, "create_playlist.html", {
                "songs": Song.objects.all(),
                "playlists": Playlist.objects.all(),
                "error": f"Failed to add songs to playlist: {str(e)}"
            })
    
    # If it's a GET request, redirect to create_playlist
    return redirect('create_playlist')


# New category page views
def new_releases_view(request):
    songs = Song.objects.all().order_by('-created_at')[:20]  # Get latest songs
    playlists = Playlist.objects.all()
    categories = Category.objects.all()
    
    context = {
        'songs': songs,
        'playlists': playlists,
        'categories': categories,
        'page_title': 'New Releases'
    }
    return render(request, 'new_releases.html', context)

def events_view(request):
    playlists = Playlist.objects.all()
    categories = Category.objects.all()
    
    context = {
        'playlists': playlists,
        'categories': categories,
        'page_title': 'Events'
    }
    return render(request, 'events.html', context)

# def charts_view(request):
#     songs = Song.objects.all().order_by('-play_count')[:20]  # Get most played songs
#     playlists = Playlist.objects.all()
#     categories = Category.objects.all()
    
#     context = {
#         'songs': songs,
#         'playlists': playlists,
#         'categories': categories,
#         'page_title': 'Charts'
#     }
#     return render(request, 'charts.html', context)

def for_you_view(request):
    songs = Song.objects.all()
    playlists = Playlist.objects.all()
    categories = Category.objects.all()
    
    context = {
        'songs': songs,
        'playlists': playlists,
        'categories': categories,
        'page_title': 'For You'
    }
    return render(request, 'for_you.html', context)

# @login_required
@login_required(login_url='song_list')
@require_POST
def like_song(request):
    song_id = request.POST.get('song_id')
    if not song_id:
        return JsonResponse({'success': False, 'error': 'No song ID provided'}, status=400)
    
    try:
        song = Song.objects.get(id=song_id)
        user = request.user
        
        # Toggle like status
        if user in song.likes.all():
            # User already liked the song, remove the like
            song.likes.remove(user)
            liked = False
        else:
            # User hasn't liked the song, add the like
            song.likes.add(user)
            liked = True
        
        # Get updated count for response
        likes_count = song.likes.count()
        
        return JsonResponse({
            'success': True,
            'liked': liked,
            'likes_count': likes_count
        })
    except Song.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Song not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500) 

def charts_view(request):
    # Use a regular order since play_count doesn't exist
    songs = Song.objects.all()[:20]  # Get first 20 songs instead of ordering by play_count
    playlists = Playlist.objects.all()
    categories = Category.objects.all()
    
    context = {
        'songs': songs,
        'playlists': playlists,
        'categories': categories,
        'page_title': 'Charts'
    }
    return render(request, 'charts.html', context)



# User Authentication Views
def user_signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            
            # Update user profile with additional info
            profile = user.profile
            profile.name = form.cleaned_data.get('name')
            profile.dob = form.cleaned_data.get('dob')
            profile.country = form.cleaned_data.get('country')
            if 'profile_image' in request.FILES:
                profile.profile_image = request.FILES['profile_image']
            profile.save()
            
            # Log the user in
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('song_list')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserRegistrationForm()
    
    categories = Category.objects.all()
    return render(request, 'accounts/signup.html', {
        'form': form,
        'categories': categories,
        'page_title': 'Sign Up'
    })

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('song_list')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()
    
    categories = Category.objects.all()
    return render(request, 'accounts/login.html', {
        'form': form,
        'categories': categories,
        'page_title': 'Log In'
    })

def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('song_list')

@login_required
def profile_view(request):
    categories = Category.objects.all()
    return render(request, 'accounts/profile.html', {
        'categories': categories,
        'page_title': 'My Profile'
    }) 