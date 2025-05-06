from django.shortcuts import render, redirect, get_object_or_404
from ReviewApp.models import UserReview
from MovieDBApp.models import UserProfile, Movie, Favorite
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests

def postComment(request):
    if request.method == "POST":
        # Get the movie ID from the form
        # Using 'id' instead of 'movie_id' to match Movie model
        movie_id = request.POST.get("movie_id")
        
        # Print debug information
        print(f"POST data: {request.POST}")
        print(f"Movie ID from form: {movie_id}")
        
        if not movie_id:
            messages.error(request, "Movie ID is missing")
            return redirect('index')
            
        # Get JWT token from cookie first, then try form if not in cookie
        jwt_token = request.COOKIES.get('jwt_token')
        if not jwt_token:
            # Try to get token from form as fallback
            jwt_token = request.POST.get('jwt_token')
            
        if not jwt_token:
            messages.error(request, "You must be logged in to post comments")
            return redirect('login')
        
        comment = request.POST.get("comment")
        if not comment:
            messages.error(request, "Comment cannot be empty")
            # Find the movie to redirect back to its page
            try:
                # Use 'id' instead of 'movie_id' to match Movie model
                movie = Movie.objects.get(id=movie_id)
                return redirect('movie_detail', title=movie.title)
            except Movie.DoesNotExist:
                return redirect('index')
        
        try:
            # Get user info from JWT token
            headers = {"Authorization": f"Bearer {jwt_token}"}
            # Make sure this URL matches exactly with your Flask backend
            user_response = requests.get("http://127.0.0.1:5000/api/user_info", headers=headers)
            
            print(f"User response status: {user_response.status_code}")  # Debug line
            print(f"User response content: {user_response.text}")  # Debug line
            
            if user_response.status_code == 200:
                user_data = user_response.json()
                username = user_data.get('name')
                
                if not username:
                    messages.error(request, "Could not identify user from token")
                    # Find the movie to redirect back to its page
                    try:
                        movie = Movie.objects.get(id=movie_id)
                        return redirect('movie_detail', title=movie.title)
                    except Movie.DoesNotExist:
                        return redirect('index')
                
                # Get the movie object using 'id' instead of 'movie_id'
                try:
                    movie = Movie.objects.get(id=movie_id)
                except Movie.DoesNotExist:
                    messages.error(request, f"Could not find movie with ID: {movie_id}")
                    return redirect('index')
                
                # Get or create the user
                try:
                    user, created = User.objects.get_or_create(username=username)
                except Exception as e:
                    messages.error(request, f"User error: {str(e)}")
                    return redirect('movie_detail', title=movie.title)
                
                # Create and save the review
                try:
                    review = UserReview(
                        comment=comment,
                        user=user,
                        movie=movie
                    )
                    review.save()
                    
                    messages.success(request, "Your comment has been posted successfully")
                except Exception as e:
                    messages.error(request, f"Could not save comment: {str(e)}")
                
                # Redirect to the movie detail page using title
                return redirect('movie_detail', title=movie.title)
            else:
                # Token validation failed
                response = redirect('login')
                response.delete_cookie('jwt_token')
                messages.error(request, f"Authentication failed with status {user_response.status_code}. Please log in again.")
                return response
                
        except requests.RequestException as e:
            print(f"Request error: {str(e)}")  # Debug line
            messages.error(request, f"Error connecting to authentication service: {str(e)}")
            # Try to find the movie and redirect back
            try:
                movie = Movie.objects.get(id=movie_id)
                return redirect('movie_detail', title=movie.title)
            except Movie.DoesNotExist:
                return redirect('index')
        except Exception as e:
            print(f"General error: {str(e)}")  # Debug line
            messages.error(request, f"An error occurred: {str(e)}")
            # Try to find the movie and redirect back
            try:
                movie = Movie.objects.get(id=movie_id)
                return redirect('movie_detail', title=movie.title)
            except Movie.DoesNotExist:
                return redirect('index')

    # If not POST or some other issue
    return redirect('index')