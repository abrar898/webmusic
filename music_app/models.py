from django.db import models
from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser

# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True)
#     date_joined = models.DateTimeField(auto_now_add=True)
#     last_login = models.DateTimeField(null=True, blank=True)

    # groups = models.ManyToManyField(
    #     "auth.Group",
    #     related_name="customuser_set",
    #     blank=True,
    #     help_text="The groups this user belongs to."
    # )
    # user_permissions = models.ManyToManyField(
    #     "auth.Permission",
    #     related_name="customuser_permissions",
    #     blank=True,
    #     help_text="Specific permissions for this user."
    # )

    # def __str__(self):
    #     return self.username


class Artist(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='artist_images/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class Album(models.Model):
    name = models.CharField(max_length=200)
    cover_image = models.ImageField(upload_to='album_covers/', blank=True, null=True)
    release_date = models.DateField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    
    def __str__(self):
        return f"{self.name} by {self.artist.name}"

class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    # image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    def __str__(self):
        return self.name

class Song(models.Model):
    title = models.CharField(max_length=200)
    audio_file = models.FileField(upload_to='songs/')
    image = models.ImageField(upload_to='song_images/', blank=True, null=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs')
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, related_name='songs', blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name='songs')
    likes = models.ManyToManyField(User, related_name='liked_songs', blank=True)
    downloaded_by = models.ManyToManyField(User, related_name='downloaded_songs', blank=True)
    play_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.title
