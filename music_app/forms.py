from django import forms
# from .models import CustomUser
from .models import Song
from django.contrib.auth.models import User
from .models import Artist, Album, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

class SignupForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

   
        # model = CustomUser
    class Meta:
        model=User
        fields = ['username', 'email', 'password1', 'password2']



class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'audio_file', 'image','artist', 'album', 'categories']
        
class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'bio']

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['name', 'cover_image', 'release_date', 'artist']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
