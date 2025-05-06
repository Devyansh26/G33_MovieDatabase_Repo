from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()

db = SQLAlchemy()


class User(db.Model, UserMixin):


    _tablename_ = "user"


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(250), nullable=False)
    mobile = db.Column(db.String(10), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="user")


    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')


    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)



class Action(db.Model):
    __tablename__ = "action"

    movie_id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    image = db.Column(db.String(500))
    director = db.Column(db.String(100))
    writer = db.Column(db.String(200))
    cast = db.Column(db.String(500))
    genre = db.Column(db.String(100))
    language = db.Column(db.String(50))
    country = db.Column(db.String(50))
    description= db.Column(db.String(500))


    def __repr__(self):
        return f"movie_id:{self.movie_id} title:{self.title} year: {self.year} rating: {self.rating} image: {self.image} director: {self.director} writer: {self.writer} genre: {self.genre} cast: {self.cast} language: {self.language} country: {self.country} description: {self.description}"


class Comedy(db.Model):
    __tablename__ = "comedy"

    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    image = db.Column(db.String(500))
    director = db.Column(db.String(100))
    writer = db.Column(db.String(200))
    cast = db.Column(db.String(500))
    genre = db.Column(db.String(100))
    language = db.Column(db.String(50))
    country = db.Column(db.String(50))
    description= db.Column(db.String(500))


    def __repr__(self):
        return f"movie_id:{self.movie_id} title:{self.title} year: {self.year} rating: {self.rating} image: {self.image} director: {self.director} writer: {self.writer} genre: {self.genre} cast: {self.cast} language: {self.language} country: {self.country} description: {self.description} "


class Drama(db.Model):
    __tablename__ = "drama"

    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    image = db.Column(db.String(900))
    director = db.Column(db.String(100))
    writer = db.Column(db.String(200))
    cast = db.Column(db.String(500))
    genre = db.Column(db.String(100))
    language = db.Column(db.String(50))
    country = db.Column(db.String(50))
    description= db.Column(db.String(500))



    def __repr__(self):
        return f"movie_id:{self.movie_id} title:{self.title} year: {self.year} rating: {self.rating} image: {self.image} director: {self.director} writer: {self.writer} genre: {self.genre} cast: {self.cast} language: {self.language} country: {self.country} description: {self.description}"


class SciFi(db.Model):
    __tablename__ = "scifi"

    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    image = db.Column(db.String(900))
    director = db.Column(db.String(100))
    writer = db.Column(db.String(200))
    cast = db.Column(db.String(500))
    genre = db.Column(db.String(100))
    language = db.Column(db.String(50))
    country = db.Column(db.String(50))
    description= db.Column(db.String(500))


    def __repr__(self):
        return f"movie_id:{self.movie_id} title:{self.title} year: {self.year} rating: {self.rating} image: {self.image} director: {self.director} writer: {self.writer} genre: {self.genre} cast: {self.cast} language: {self.language} country: {self.country} description: {self.description} "



class Horror(db.Model):
    __tablename__ = "horror"

    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    image = db.Column(db.String(900))
    director = db.Column(db.String(100))
    writer = db.Column(db.String(200))
    cast = db.Column(db.String(500))
    genre = db.Column(db.String(100))
    language = db.Column(db.String(50))
    country = db.Column(db.String(50))
    description= db.Column(db.String(500))


    def __repr__(self):
        return f"movie_id:{self.movie_id} title:{self.title} year: {self.year} rating: {self.rating} image: {self.image} director: {self.director} writer: {self.writer} genre: {self.genre} cast: {self.cast} language: {self.language} country: {self.country} description: {self.description} "
