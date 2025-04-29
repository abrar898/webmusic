from django.db.models import Q
from music_app.models import Song  # Import your Song model

def search_songs(search_query):
    if search_query:
        return Song.objects.filter(
            Q(title__icontains=search_query) 
            # Q(artist__name__icontains=search_query) |  # Ensure ForeignKey lookup
            # Q(album__title__icontains=search_query)    # Ensure ForeignKey lookup
        )
    else:
        return Song.objects.all()
