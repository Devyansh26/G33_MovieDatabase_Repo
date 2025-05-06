from flask import Flask, request, jsonify,redirect,flash,url_for,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required,get_jwt,get_jwt_identity
from datetime import timedelta
from models.model import User,db,Action,Drama,Comedy,SciFi,Horror
from functools import wraps
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user




jwt = JWTManager()


class RegisterAPI(Resource):
    def post(self):
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        mobile = data.get('mobile')

        if password != confirm_password:
            return {'message': 'Passwords do not match!'}, 400

        if User.query.filter_by(email=email).first():
            return {'message': 'Email already exists!'}, 400

        new_user = User(name=name, email=email, mobile=mobile)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'Registration successful!'}, 201


class LoginAPI(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        user = User.query.filter_by(email=email, role=role).first()
        if user and user.check_password(password):
            # ✅ Use only string ID as identity
            access_token = create_access_token(
                identity=str(user.id),  # identity MUST be a string
                additional_claims={     # optional: extra data you want to include
                    "email": user.email,
                    "role": user.role
                }
            )
            return {
                "message": "Login successful!",
                "access_token": access_token
            }, 200

        return {"message": "Invalid credentials!"}, 401
    
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get("role") != "admin":
            return {"message": "Admin access required"}, 403
        return func(*args, **kwargs)
    return wrapper


genre_map = {
    "action": Action,
    "comedy": Comedy,
    "drama": Drama,
    "scifi": SciFi,
    "horror": Horror,
}
class AddMovieAPI(Resource):
    @jwt_required()
    @admin_required
    def post(self):
        data = request.get_json()
        title = data.get("title")
        year = data.get("year")
        rating = data.get("rating")
        image_url = data.get("image")
        genre = data.get("genre", "").lower()

        if not (title and year and rating and image_url and genre):
            return {"message": "Missing required fields"}, 400

        try:
            year = int(year)
            rating = float(rating)
        except ValueError:
            return {"message": "Invalid year or rating"}, 400

        if genre not in genre_map:
            return {"message": "Invalid genre"}, 400

        new_movie = genre_map[genre](
            title=title,
            year=year,
            rating=rating,
            image=image_url
        )

        db.session.add(new_movie)
        db.session.commit()

        return {"message": "Movie added successfully"}, 201


class MoviesByGenreAPI(Resource):
    def get(self, genre):
        genre = genre.lower()

        if genre not in genre_map:
            return {"message": "Invalid genre"}, 400

        movies = genre_map[genre].query.all()

        serialized = [
            {
                "id": movie.movie_id,
                "title": movie.title,
                "year": movie.year,
                "rating": movie.rating,
                "image": movie.image
            } for movie in movies
        ]

        return {genre: serialized}, 200


class MovieDetailAPI(Resource):
    def get(self, genre, movie_id):
        genre = genre.lower()

        if genre not in genre_map:
            return {"message": "Invalid genre"}, 400

        movie_model = genre_map[genre]
        movie = movie_model.query.get_or_404(movie_id)

        return {
            "id": movie.movie_id,
            "title": movie.title,
            "year": movie.year,
            "rating": movie.rating,
            "director": movie.director,
            "writer": movie.writer,
            "cast": movie.cast,
            "language": movie.language,
            "country": movie.country,
            "description": movie.description,
            "image": movie.image
        }, 200

    @jwt_required()
    @admin_required
    def put(self, genre, movie_id):
        genre = genre.lower()

        if genre not in genre_map:
            return {"message": "Invalid genre"}, 400

        movie_model = genre_map[genre]
        movie = movie_model.query.get_or_404(movie_id)

        data = request.get_json()

        try:
            movie.title = data.get("title", movie.title)
            movie.year = int(data.get("year", movie.year))
            movie.rating = float(data.get("rating", movie.rating))
            movie.director = data.get("director", movie.director)
            movie.writer = data.get("writer", movie.writer)
            movie.cast = data.get("cast", movie.cast)
            movie.language = data.get("language", movie.language)
            movie.country = data.get("country", movie.country)
            movie.description = data.get("description", movie.description)
            movie.image = data.get("image", movie.image)

            db.session.commit()

            return {"message": "Movie updated successfully"}, 200
        except Exception as e:
            return {"message": f"Update failed: {str(e)}"}, 400

    @jwt_required()
    @admin_required
    def delete(self, genre, movie_id):
        genre = genre.lower()

        if genre not in genre_map:
            return {"message": "Invalid genre"}, 400

        movie_model = genre_map[genre]
        movie = movie_model.query.get_or_404(movie_id)

        db.session.delete(movie)
        db.session.commit()

        return {"message": "Movie deleted successfully"}, 200



class UserInfoAPI(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()  # string id if you're following previous guidance

        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "mobile": user.mobile
        }, 200
    


class UpdateProfileAPI(Resource):
    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return {"message": "User not found"}, 404

        data = request.get_json()

        name = data.get('name')
        email = data.get('email')
        mobile = data.get('mobile')
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if name:
            user.name = name
        if email:
            user.email = email
        if mobile:
            user.mobile = mobile

        # Handle password change if requested
        if any([old_password, new_password, confirm_password]):
            if not all([old_password, new_password, confirm_password]):
                return {"message": "To change password, provide old, new, and confirm passwords."}, 400
            if not user.check_password(old_password):
                return {"message": "Old password is incorrect"}, 400
            if new_password != confirm_password:
                return {"message": "New passwords do not match"}, 400
            user.set_password(new_password)

        db.session.commit()
        return {"message": "Profile updated successfully"}, 200
    

