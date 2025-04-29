from django.shortcuts import render, redirect, get_object_or_404
from .forms import SongForm
from .models import Category, Song, Artist, Album
# from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .forms import ArtistForm, AlbumForm, CategoryForm
from django.contrib.auth import logout
from django.contrib import messages
from .forms import SignupForm, LoginForm
from playlists.models import Playlist




def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)  # Auto-login after signup
            messages.success(request, "Signup successful! Welcome, " + user.username)
            return redirect('login')
        else:
            messages.error(request, "Signup failed. Please check the form.")
    else:
        form = SignupForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


# Login View
def login_view(request):
    # if request.user.is_authenticated:
    #     return redirect('home')  # Redirect if already logged in

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # login(request, user)
            messages.success(request, "Login successful! Welcome back, " + user.username)
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})





# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')  # Redirect to login page after logout

def add_artist(request):
    if request.method == "POST":
        form = ArtistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("upload_song")  
    else:
        form = ArtistForm()
    return render(request, "add_artist.html", {"form": form})

def add_album(request):
    if request.method == "POST":
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("upload_song")
    else:
        form = AlbumForm()
    return render(request, "add_album.html", {"form": form})

def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("upload_song")
    else:
        form = CategoryForm()
    return render(request, "add_category.html", {"form": form})

def home(request):
    # Get all artists from the database
    artists = Artist.objects.all()
    songs = Song.objects.all()
    return render(request, 'home.html', {'artists': artists, 'songs': songs})

def category_list(request):
    """Display all categories."""
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def song_list(request):
    songs = Song.objects.all()
    playlists = Playlist.objects.all()
    categories = Category.objects.all()
    
    category_param = request.GET.get('category')
    if category_param:
        if category_param == 'new-releases':
            return redirect('new_releases')
        elif category_param == 'events':
            return redirect('events')
        elif category_param == 'charts':
            return redirect('charts')
        elif category_param == 'for-you':
            return redirect('for_you')
    
    context = {
        'songs': songs,
        'playlists': playlists,
        'categories': categories,
        'page_title': 'Home'
    }
    return render(request, 'index.html',context)

# def song_list(request):
#     songs = Song.objects.all()
#     playlists = Playlist.objects.all()
#     categories = Category.objects.all()
    
#     category_param = request.GET.get('category')
#     if category_param:
#         if category_param == 'new-releases':
#             return redirect('new_releases')
#         elif category_param == 'events':
#             return redirect('events')
#         elif category_param == 'charts':
#             return redirect('charts')
#         elif category_param == 'for-you':
#             return redirect('for_you')
    
#     context = {
#         'songs': songs,
#         'playlists': playlists,
#         'categories': categories,
#         'page_title': 'Home'
#     }
#     return render(request, 'song_list.html', context)



def upload_song(request):
    if request.method == "POST":
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save(commit=False)
            song.artist = request.user  # Assign logged-in user as artist
            song.save()
            form.save_m2m()  # Save many-to-many fields
            return redirect('home')  
    else:
        form = SongForm()
    
    return render(request, 'upload_song.html', {'form': form})



def artist_detail(request, artist_id):
    """Display artist details and their albums."""
    artist = get_object_or_404(Artist, id=artist_id)
    albums = Album.objects.filter(artist=artist)
    songs = Song.objects.filter(artist=artist)
    return render(request, 'artist_detail.html', {
        'artist': artist,
        'albums': albums,
        'songs': songs
    })

def category_detail(request, category_id):
    """Display songs in a specific genre/category."""
    category = get_object_or_404(Category, id=category_id)
    songs = Song.objects.filter(categories=category)
    
    # Get unique artists for the "Artists in this genre" section
    unique_artists = []
    artist_ids = set()
    for song in songs:
        if song.artist.id not in artist_ids:
            unique_artists.append(song.artist)
            artist_ids.add(song.artist.id)
    
    return render(request, 'category_detail.html', {
        'category': category,
        'songs': songs,
        'unique_artists': unique_artists[:10]  # Limit to 10 artists
    })