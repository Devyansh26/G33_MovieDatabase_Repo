from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Movie, Favorite
import random
from ReviewApp.models import UserReview
from django.http import JsonResponse
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import requests
from functools import wraps
import functools
# Create your views here.


api_key = '15c784b'


register_url = "http://127.0.0.1:5000/api/register"
login_url = "http://127.0.0.1:5000/api/login"
user_info_url = "http://127.0.0.1:5000/api/user_info"
update_profile_url = "http://localhost:5000/api/update_profile"  

def jwt_login_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        jwt_token = request.COOKIES.get('jwt_token')
        
        if not jwt_token:
            messages.error(request, 'Please login to access this page')
            return redirect('login')
            
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = requests.get(user_info_url, headers=headers)
        
        if response.status_code != 200:
            response = redirect('login')
            response.delete_cookie('jwt_token')
            messages.error(request, 'Your session has expired. Please login again.')
            return response
            
        request.user_data = response.json()
        
        return view_func(request, *args, **kwargs)
    return wrapper




def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        login_data = {
            "email": email,
            "password": password,
            "role": role
        }
        login_response = requests.post(login_url, json=login_data)

        if login_response.status_code == 200:
            jwt_token = login_response.json()['access_token']
            print(f"JWT Token: {jwt_token}")
            
            response = redirect('index')
            
            response.set_cookie(
                'jwt_token', 
                jwt_token, 
                httponly=True,  
                secure=True, 
                samesite='Lax'
            )
            
            return response
        else:
            print(f"Login failed: {login_response.status_code}")
            return render(request, 'login.html', {'error': 'Login failed. Please check your credentials.'})

    return render(request, 'login.html')


def index(request):
    movies=[
        {'title':'The Dark Knight','year':1996,'rating':4.4,'image':'https://m.media-amazon.com/images/I/81IfoBox2TL._AC_UF1000,1000_QL80_.jpg'},
        {'title':'Inception','year':1998,'rating':4.3,'image':'https://th.bing.com/th/id/OIP.ps02Cq1ZLtzBEPPpSVttKgHaLH?rs=1&pid=ImgDetMain'},
        {'title':'Barfi','year':1984,'rating':4.7,'image':'https://th.bing.com/th/id/R.14502782cd5dc58bec86aded621c31c6?rik=4aiMWzXin57PMQ&riu=http%3a%2f%2f4.bp.blogspot.com%2f-q3xjcBGBQVA%2fUFIit1azIGI%2fAAAAAAAAgRY%2fFXLXNPFKKbc%2fs1600%2fbarfi_poster.jpg&ehk=snW9hU427Wgyy3xhrQ42IJhsXxveNBmPh%2biVGKfBvWI%3d&risl=&pid=ImgRaw&r=0'},
        {'title':'3 idiots','year':1999,'rating':4.3,'image':'https://th.bing.com/th/id/OIP.qeTgeLDl6ZpMpEaGSff_9AHaJ9?rs=1&pid=ImgDetMain'},
    ]
    
    jwt_token = request.COOKIES.get('jwt_token')
    
    if not jwt_token:
        jwt_token = request.GET.get('jwt_token')
    
    user_data = None
    if jwt_token:
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = requests.get("http://127.0.0.1:5000/api/user_info", headers=headers)

        if response.status_code == 200:
            user_data = response.json()
    
    context = {
        'is_authenticated': bool(user_data),
        'username': user_data.get('username') if user_data else None,
        'movies': movies,
        'jwt_token': jwt_token if jwt_token else None
    }
    
    response = render(request, 'index.html', context)
    
    if not request.COOKIES.get('jwt_token') and jwt_token:
        response.set_cookie(
            'jwt_token', 
            jwt_token, 
            httponly=True,
            secure=True,
            samesite='Lax'
        )
    
    return response

def register(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        
        register_data = {
            "name": username,
            "email": email,
            "mobile": mobile,
            "password": password,
            "confirm_password": cpassword
        }
        register_response = requests.post(register_url, json=register_data)


        if register_response.status_code == 201:
            print("User registered successfully.")
            return redirect('login')
        else:
            print(f"User registration failed: {register_response.status_code}")
            print(f"Response: {register_response.text}")

            return render(request, 'register.html')


    return render(request, 'register.html')

@jwt_login_required
def profile(request):
    user_data = request.user_data
    
    user_id = user_data.get('id')  
    
    try:
        favorites = Favorite.objects.filter(user_id=user_id).select_related('movie').order_by('-date_added')
        
        valid_favorites = []
        for favorite in favorites:
            if favorite.movie and hasattr(favorite.movie, 'movie_id'):
                valid_favorites.append(favorite)
            else:
                favorite.delete()
                
        context = {
            'user': user_data,
            'favorites': valid_favorites,
            'jwt_token': request.COOKIES.get('jwt_token'), 
        }
        return render(request, 'profile.html', context)
    except Exception as e:
        messages.error(request, f'Error loading favorites: {str(e)}')
        context = {
            'user': user_data,
            'favorites': [],
            'jwt_token': request.COOKIES.get('jwt_token'), 
        }
        return render(request, 'profile.html', context)
@jwt_login_required
def update_profile(request):
    if request.method == 'POST':
        try:
            jwt_token = request.COOKIES.get('jwt_token')
            if not jwt_token:
                messages.error(request, 'Authentication token is missing')
                return redirect('profile')
                
            headers = {"Authorization": f"Bearer {jwt_token}"}
            user_data = request.user_data
            
            # Get form data
            new_password = request.POST.get('new_password')
            old_password = request.POST.get('old_password')
            
            update_data = {
                "user_id": user_data.get('id'),
                "name": request.POST.get('name'),
                "email": request.POST.get('email'),
                "mobile": request.POST.get('mobile')
            }
            
            if new_password:
                if not old_password:
                    messages.error(request, 'Current password is required to change password')
                    return redirect('profile')
                    
                update_data.update({
                    "old_password": old_password,
                    "new_password": new_password,
                    "confirm_password": request.POST.get('confirm_password')
                })
            
            update_response = requests.put(
                update_profile_url, 
                json=update_data,
                headers=headers
            )
            
            if update_response.status_code == 200:
                messages.success(request, 'Profile updated successfully')
                if new_password:
                    response = redirect('login')
                    response.delete_cookie('jwt_token')
                    return response
                return redirect('profile')
            else:
                error_message = update_response.json().get('message', 'Profile update failed')
                messages.error(request, error_message)
                
        except Exception as e:
            messages.error(request, f'Profile update failed: {str(e)}')
            
    return redirect('profile')


genre_movies = {
    "Action": ["Mad Max", "Die Hard", "John Wick", "Gladiator", "The Dark Knight", "Inception", "Mission Impossible"],
    "Comedy": ["Superbad", "Step Brothers", "The Mask", "The Hangover", "Anchorman", "Dumb and Dumber", "Borat"],
    "Drama": ["Forrest Gump", "The Shawshank Redemption", "The Godfather", "Fight Club", "A Beautiful Mind", "12 Angry Men", "The Pursuit of Happyness"],
    "Thriller": ["Se7en", "Gone Girl", "Shutter Island", "Prisoners", "Zodiac", "The Silence of the Lambs", "The Girl with the Dragon Tattoo"],
    "Horror": ["The Conjuring", "Hereditary", "Get Out", "A Nightmare on Elm Street", "The Exorcist", "It", "The Shining"]
}

def fetch_and_store_movie(title):
    existing_movie = Movie.objects.filter(title__iexact=title).first()
    if existing_movie:
        return existing_movie
    
    # If not in database, fetch from API
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"
    response = requests.get(url)
    data = response.json()
    
    if data.get('Response') == 'True':
        Movie.objects.update_or_create(
                imdb_id=data['imdbID'],
                defaults={
                    'imdb_id': data['imdbID'],
                    'title': data['Title'],
                    'year': data['Year'],
                    'genre': data['Genre'],
                    'director': data['Director'],
                    'actors': data['Actors'],
                    'plot': data['Plot'],
                    'poster_url': data['Poster'],
                    'imdb_rating': data['imdbRating'],
                    'language': data['Language'],

                }
                )  
  

def fetch_all_movies():
    for genre, titles in genre_movies.items():
        for title in titles:
            fetch_and_store_movie(title)

def movie_list(request):
    if Movie.objects.count() < 20: 
        fetch_all_movies()
    
    selected_movies = {}
    
    jwt_token = request.COOKIES.get('jwt_token')
    user_data = None
    
    if jwt_token:
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = requests.get(user_info_url, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
    
  
    for genre_name in genre_movies.keys():
        
        genre_db_movies = Movie.objects.filter(genre__icontains=genre_name)[:4]
        
        if genre_db_movies.count() < 4:
            for title in genre_movies[genre_name]:
                fetch_and_store_movie(title)
      
            genre_db_movies = Movie.objects.filter(genre__icontains=genre_name)[:4]
        
        selected_movies[genre_name] = genre_db_movies
    
    context = {
        'selected_movies': selected_movies,
        'is_authenticated': bool(user_data),
        'username': user_data.get('username') if user_data else None,
        'user_data': user_data, 
        'jwt_token': jwt_token if jwt_token else None
    }
    
    return render(request, 'movies.html', context)

def genre_all_movies(request, genre_name):
    """Display all movies of a specific genre, fetching from database"""
    if genre_name in genre_movies:
        for title in genre_movies[genre_name]:
            fetch_and_store_movie(title)
    
    movies = Movie.objects.filter(genre__icontains=genre_name)
    
    return render(request, 'genre_all.html', {'genre': genre_name, 'movies': movies})


def movie_detail(request, title):
    """Display details of a specific movie"""
    movie = Movie.objects.filter(title__iexact=title).first()
    
    if not movie:
        movie = fetch_and_store_movie(title)
    
    jwt_token = request.COOKIES.get('jwt_token')
    user_data = None
    
    if jwt_token:
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = requests.get(user_info_url, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
    
    comments = UserReview.objects.filter(movie=movie).order_by('-timestamp')
    
    for comment in comments:
        comment.username = comment.user.username
    
    if movie:
        return render(request, 'movie_detail.html', {
            'movie': movie, 
            'comments': comments,
            'jwt_token': jwt_token,
            'user_data': user_data
        })
    else:
        return render(request, 'movie_detail.html', {'error': 'Movie not found'})

@login_required
def add_to_favorites(request, movie_id):
    try:
        movie = get_object_or_404(Movie, movie_id=movie_id)
        user = request.user
        
        favorite = Favorite.objects.filter(user=user, movie=movie).first()
        
        if favorite:
            favorite.delete()
            messages.success(request, f'"{movie.title}" removed from your favorites!')
        else:
            Favorite.objects.create(user=user, movie=movie)
            messages.success(request, f'"{movie.title}" added to your favorites!')
    except Exception as e:
        messages.error(request, f'Error managing favorites: {str(e)}')
    
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('movie_detail', movie_id=movie_id)

@login_required
def remove_favorite(request, movie_id):
    if request.method == 'POST':
        try:
            movie = get_object_or_404(Movie, movie_id=movie_id)
            favorite = Favorite.objects.filter(user=request.user, movie=movie).first()
            if favorite:
                favorite.delete()
                messages.success(request, f'"{movie.title}" removed from favorites')
            else:
                messages.error(request, f'Movie not found in your favorites')
        except Exception as e:
            messages.error(request, f'Error removing favorite: {str(e)}')
    return redirect('profile')


def logout_view(request):
    response = redirect('index')
    response.delete_cookie('jwt_token')
    
    messages.success(request, 'Logout successful')
    return response

def contact(request):
    jwt_token = request.COOKIES.get('jwt_token')
    user_data = None
    
    if jwt_token:
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = requests.get(user_info_url, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
    
    context = {
        'is_authenticated': bool(user_data),
        'username': user_data.get('username') if user_data else None,
        'user_data': user_data,
        'jwt_token': jwt_token if jwt_token else None
    }
    
    return render(request, 'contact.html', context)

def about(request):
    jwt_token = request.COOKIES.get('jwt_token')
    user_data = None
    
    if jwt_token:
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = requests.get(user_info_url, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
    
    context = {
        'is_authenticated': bool(user_data),
        'username': user_data.get('username') if user_data else None,
        'user_data': user_data,
        'jwt_token': jwt_token if jwt_token else None
    }
    
    return render(request, 'about.html', context)


def search_movie(request):
    query = request.GET.get('q')
    movie = None
    error = None

    if query:
        url = f"http://www.omdbapi.com/?apikey={api_key}&t={query}"
        response = requests.get(url)
        data = response.json()

        if data.get('Response') == 'True':
            movie = data
        else:
            error = data.get('Error', 'Movie not found.')

    return render(request, 'search_result.html', {'movie': movie, 'error': error, 'query': query})



def admin_required(view_func):
    """
    Decorator that checks if the user is authenticated and has admin role
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        jwt_token = request.COOKIES.get('jwt_token')
        
        if not jwt_token:
            messages.error(request, 'Please login to access this page')
            return redirect('login')
            
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = requests.get(user_info_url, headers=headers)
        
        if response.status_code != 200:
            response = redirect('login')
            response.delete_cookie('jwt_token')
            messages.error(request, 'Your session has expired. Please login again.')
            return response
        
        user_data = response.json()
        
        if user_data.get('role') != 'admin':
            messages.error(request, 'You do not have permission to access this page')
            return redirect('index')
            
        # Add user data to the request
        request.user_data = user_data
        
        return view_func(request, *args, **kwargs)
    return wrapper

def search_movie_json(request):
    query = request.GET.get('q')
    
    if not query:
        return JsonResponse({'error': 'No search query provided'})
    
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={query}"
    response = requests.get(url)
    data = response.json()
    
    if data.get('Response') == 'True':
        return JsonResponse(data)
    else:
        return JsonResponse({'error': data.get('Error', 'Movie not found')})



@admin_required
def add_movie(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        year = request.POST.get('year')
        genre = request.POST.get('genre')
        director = request.POST.get('director')
        actors = request.POST.get('actors')
        plot = request.POST.get('plot')
        poster_url = request.POST.get('poster_url')
        imdb_rating = request.POST.get('imdb_rating')
        language = request.POST.get('language')
        trailer = request.POST.get('trailer')
        
        # Try to fetch from OMDB API first if title is provided
        if title and not imdb_rating:
            url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"
            response = requests.get(url)
            data = response.json()
            
            if data.get('Response') == 'True':
                # Pre-fill form with API data
                title = data.get('Title', title)
                year = data.get('Year', year)
                genre = data.get('Genre', genre)
                director = data.get('Director', director)
                actors = data.get('Actors', actors)
                plot = data.get('Plot', plot)
                poster_url = data.get('Poster', poster_url)
                imdb_rating = data.get('imdbRating', imdb_rating)
                language = data.get('Language', language)
                imdb_id = data.get('imdbID', None)
                
                movie = Movie(
                    title=title,
                    year=year,
                    genre=genre,
                    director=director,
                    actors=actors,
                    plot=plot,
                    poster_url=poster_url,
                    imdb_rating=imdb_rating,
                    language=language,
                    trailer=trailer,
                    imdb_id=imdb_id
                )
                movie.save()
                messages.success(request, f'"{title}" has been added successfully!')
                return redirect('movie')
            else:
                pass
        
        if title:
            movie = Movie(
                title=title,
                year=year,
                genre=genre,
                director=director,
                actors=actors,
                plot=plot,
                poster_url=poster_url,
                imdb_rating=imdb_rating,
                language=language,
                trailer=trailer
            )
            movie.save()
            messages.success(request, f'"{title}" has been added successfully!')
            return redirect('movie')
        else:
            messages.error(request, 'Movie title is required')
    
    # For GET request or form errors
    return render(request, 'add_movie.html')


@admin_required
def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    
    if request.method == 'POST':
        movie.title = request.POST.get('title', movie.title)
        movie.year = request.POST.get('year', movie.year)
        movie.genre = request.POST.get('genre', movie.genre)
        movie.director = request.POST.get('director', movie.director)
        movie.actors = request.POST.get('actors', movie.actors)
        movie.plot = request.POST.get('plot', movie.plot)
        movie.poster_url = request.POST.get('poster_url', movie.poster_url)
        movie.imdb_rating = request.POST.get('imdb_rating', movie.imdb_rating)
        movie.language = request.POST.get('language', movie.language)
        movie.trailer = request.POST.get('trailer', movie.trailer)
        
        movie.save()
        messages.success(request, f'"{movie.title}" has been updated successfully!')
        return redirect('movie_detail', title=movie.title)
    
    return render(request, 'edit_movie.html', {'movie': movie})


@admin_required
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    
    if request.method == 'POST':
        movie_title = movie.title
        movie.delete()
        messages.success(request, f'"{movie_title}" has been deleted successfully!')
        return redirect('movie')
    
    return render(request, 'delete_movie.html', {'movie': movie})
