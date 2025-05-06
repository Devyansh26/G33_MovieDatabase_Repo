from django.contrib import admin
from MovieDBApp.models import Movie

# Register your models here.

class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'year', 'imdb_rating', 'director', 'language']
        



admin.site.register(Movie, MovieAdmin)


