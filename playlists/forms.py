from django import forms
from .models import Playlist
from music_app.models import Song
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import datetime

class UserRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-3 rounded bg-blue-900 border border-blue-700 text-white focus:outline-none focus:border-blue-500',
        'placeholder': 'Full Name'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'w-full px-4 py-3 rounded bg-blue-900 border border-blue-700 text-white focus:outline-none focus:border-blue-500',
        'placeholder': 'Email address'
    }))
    dob = forms.DateField(
        required=True, 
        widget=forms.DateInput(attrs={
            'class': 'w-full px-4 py-3 rounded bg-blue-900 border border-blue-700 text-white focus:outline-none focus:border-blue-500',
            'type': 'date',
            'style': 'color-scheme: dark;'
        }),
        label='Date of Birth'
    )
    country = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-3 rounded bg-blue-900 border border-blue-700 text-white focus:outline-none focus:border-blue-500',
        'placeholder': 'Country'
    }))
    profile_image = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'w-full px-4 py-3 rounded bg-blue-900 border border-blue-700 text-white focus:outline-none focus:border-blue-500',
    }))
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 rounded bg-blue-900 border border-blue-700 text-white focus:outline-none focus:border-blue-500',
            'placeholder': 'Password'
        }),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 rounded bg-blue-900 border border-blue-700 text-white focus:outline-none focus:border-blue-500',
            'placeholder': 'Confirm Password'
        }),
    )

    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'dob', 'country', 'profile_image', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded bg-blue-900 border border-blue-700 text-white focus:outline-none focus:border-blue-500',
                'placeholder': 'Username'
            }),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email
    
    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        today = datetime.date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < 13:
            raise ValidationError("You must be at least 13 years old to register.")
        return dob

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-3 rounded bg-blue-900 border border-blue-700 text-white focus:outline-none focus:border-blue-500',
        'placeholder': 'Email or Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-3 rounded bg-blue-900 border border-blue-700 text-white focus:outline-none focus:border-blue-500',
        'placeholder': 'Password'
    }))

class PlaylistForm(forms.ModelForm):
    songs = forms.ModelMultipleChoiceField(
        queryset=Song.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Playlist
        fields = ['name', 'description', 'songs']
