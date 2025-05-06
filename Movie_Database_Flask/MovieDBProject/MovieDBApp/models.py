from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


class Movie(models.Model):
    
    id = models.AutoField(primary_key=True)
    imdb_id = models.CharField(max_length=20, unique=True, null=True)  # e.g., tt1375666
    title = models.CharField(max_length=255, null=True)
    year = models.CharField(max_length=10, null=True)
    genre = models.CharField(max_length=100, null=True)
    director = models.CharField(max_length=255, null=True)
    actors = models.TextField(default="Unknown")
    plot = models.TextField(null=True)
    poster_url = models.URLField(null=True)
    imdb_rating = models.CharField(max_length=10, null=True)
    language = models.CharField(max_length=50, null=True)
    trailer = models.URLField(max_length=150 , null=True)

    def get_cast_list(self):
        """Returns the cast as a list of names"""
        if self.actors:
            return [actor.strip() for actor in self.actors.split(',')]
        return []

    def __str__(self):
        return self.title

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    email = models.EmailField(null=True, blank=True) 
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='favorited_by')
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'movie')
        
    def __str__(self):
        return f"{self.user.username}'s favorite: {self.movie.title}"

