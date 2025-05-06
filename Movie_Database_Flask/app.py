from flask import Flask,render_template,redirect,url_for,request,flash
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from functools import wraps
from flask_restful import Api
from resource.app_resource import RegisterAPI,LoginAPI,AddMovieAPI,MoviesByGenreAPI,MovieDetailAPI,UserInfoAPI,UpdateProfileAPI
from datetime import timedelta
from models.model import db,User,Action,Drama,Comedy,SciFi,Horror
from flask_jwt_extended import JWTManager, create_access_token, jwt_required


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + \
    os.path.join(basedir, "app.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SECRET_KEY"] = "Secret key"

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

db.init_app(app)


jwt = JWTManager(app) 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"






api = Api(app)



def setup_db():
    with app.app_context():
        db.create_all()



        if not Action.query.first():
            Movie1 =  Action(
    title="Mad Max: Fury Road",
    year=2015,
    rating=8.6,
    director="George Miller",
    writer="George Miller, Brendan McCarthy, Nico Lathouris",
    cast="Tom Hardy, Charlize Theron, Nicholas Hoult, Hugh Keays-Byrne, Rosie Huntington-Whiteley, Zoë Kravitz",
    genre="Action",
    language="English",
    country="Australia, USA",
    image="https://m.media-amazon.com/images/M/MV5BZTEyZWFjNDktZjQwYy00ZDNhLThhODUtZWZjMmFhNzQ5Zjg1XkEyXkFqcGc@._V1_.jpg"
)
            Movie2 =Action(
    title="The Dark Knight",
    year=2008,
    rating=9.0,
    director="Christopher Nolan",
    writer="Jonathan Nolan, Christopher Nolan, David S. Goyer",
    cast="Christian Bale, Heath Ledger, Aaron Eckhart,Michael Caine, Maggie Gyllenhaal, Gary Oldman",
    genre="Action",
    language="English",
    country="USA, UK",
    image="https://m.media-amazon.com/images/S/pv-target-images/e9a43e647b2ca70e75a3c0af046c4dfdcd712380889779cbdc2c57d94ab63902.jpg"
)
            Movie3 = Action(
    title="Avatar",
    year=2009,
    rating=7.8,
    director="James Cameron",
    writer="James Cameron",
    cast="Sam Worthington, Zoe Saldana, Sigourney Weaver, Stephen Lang, Michelle Rodriguez, Giovanni Ribisi",
    genre="Action, Adventure, Sci-Fi",
    language="English",
    country="USA, UK",
    image="https://m.media-amazon.com/images/M/MV5BMDEzMmQwZjctZWU2My00MWNlLWE0NjItMDJlYTRlNGJiZjcyXkEyXkFqcGc@._V1_.jpg"
)
            Movie4 =Action(
    title="Gravity",
    year=2013,
    rating=7.7,
    director="Alfonso Cuarón",
    writer="Alfonso Cuarón, Jonás Cuarón",
    cast="Sandra Bullock, George Clooney, Ed Harris, Orto Ignatiussen, Phaldut Sharma, Amy Warren",
    genre="Action",
    language="English",
    country="USA, UK",
    image="https://image.tmdb.org/t/p/original/aq01FtuCkjdVfSFbuYZSXIm35RD.jpg"
)


            db.session.add_all([Movie1,Movie2,Movie3,Movie4])
            db.session.commit()

        if not Comedy.query.first():
            Comedy1 = Comedy(
    title="The Hangover",
    year=2009,
    rating=7.7,
    director="Todd Phillips",
    writer="Jon Lucas, Scott Moore",
    cast="Bradley Cooper, Ed Helms, Zach Galifianakis, Justin Bartha, Heather Graham, Ken Jeong",
    genre="Comedy",
    language="English",
    country="USA",
    image="https://th.bing.com/th/id/OIP.Rt7dy6EVY4xT6wngC0jFLwHaLH?rs=1&pid=ImgDetMain"
)
            Comedy2 = Comedy(
    title="Superbad",
    year=2007,
    rating=7.6,
    director="Greg Mottola",
    writer="Seth Rogen, Evan Goldberg",
    cast="Jonah Hill, Michael Cera, Christopher Mintz-Plasse, Bill Hader, Seth Rogen, Emma Stone",
    genre="Comedy",
    language="English",
    country="USA",
    image="https://i.etsystatic.com/30490360/r/il/2504af/3277413531/il_1140xN.3277413531_8lte.jpg"
)
            Comedy3 = Comedy(
    title="Phir Hera Pheri",
    year=2006,
    rating=7.1,
    director="Neeraj Vora",
    writer="Neeraj Vora, Kader Khan",
    cast="Akshay Kumar, Suniel Shetty, Paresh Rawal, Bipasha Basu, Rimi Sen, Rajpal Yadav",
    genre="Comedy",
    language="Hindi",
    country="India",
    image="https://m.media-amazon.com/images/M/MV5BMTNkZTExMWYtMGZjMy00NGUwLWJmMWEtOThjYmZjY2Q0N2M5XkEyXkFqcGc@._V1_.jpg"
)
            Comedy4 =  Comedy(
    title="Welcome",
    year=2007,
    rating=7.0,
    director="Anees Bazmee",
    writer="Anees Bazmee, Rajiv Kaul, Praful Parekh",
    cast="Akshay Kumar, Katrina Kaif, Anil Kapoor, Nana Patekar, Paresh Rawal, Feroz Khan",
    genre="Comedy",
    language="Hindi",
    country="India",
    image="https://media-cache.cinematerial.com/p/500x/kmhrxd2m/welcome-indian-movie-poster.jpg?v=1456244622"
)
            db.session.add_all([Comedy1, Comedy2,Comedy3, Comedy4])
            db.session.commit()

        if not Drama.query.first():
            drama1 = Drama(
    title="The Godfather",
    year=1972,
    rating=9.2,
    director="Francis Ford Coppola",
    writer="Mario Puzo, Francis Ford Coppola",
    cast="Marlon Brando, Al Pacino, James Caan, Diane Keaton, Robert Duvall, Sterling Hayden",
    genre=" Drama",
    language="English, Italian",
    country="USA",
    image="https://m.media-amazon.com/images/M/MV5BNGEwYjgwOGQtYjg5ZS00Njc1LTk2ZGEtM2QwZWQ2NjdhZTE5XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg"
)
            drama2 = Drama(
    title="Forrest Gump",
    year=1994,
    rating=8.8,
    director="Robert Zemeckis",
    writer="Winston Groom, Eric Roth",
    cast="Tom Hanks, Robin Wright, Gary Sinise, Mykelti Williamson, Sally Field, Haley Joel Osment",
    genre="Drama",
    language="English",
    country="USA",
    image="https://resizing.flixster.com/hqcqFfWf1syt2OrGlbW7LDvfj9Y=/fit-in/352x330/v2/https://resizing.flixster.com/-XZAfHZM39UwaGJIFWKAE8fS0ak=/v3/t/assets/p15829_v_v13_aa.jpg"
)
            drama3=Drama(
    title="Schindler's List",
    year=1993,
    rating=9.0,
    director="Steven Spielberg",
    writer="Thomas Keneally, Steven Zaillian",
    cast="Liam Neeson, Ralph Fiennes, Ben Kingsley, Caroline Goodall, Embeth Davidtz, Jonathan Sagall",
    genre=" Drama",
    language="English, Hebrew, German, Polish",
    country="USA",
    image="https://m.media-amazon.com/images/I/81+H4lZVw+L._AC_UF1000,1000_QL80_.jpg"
)
            drama4=Drama(
    title="Fight Club",
    year=1999,
    rating=8.8,
    director="David Fincher",
    writer="Chuck Palahniuk, Jim Uhls",
    cast="Brad Pitt, Edward Norton, Helena Bonham Carter, Meat Loaf, Jared Leto, Zach Grenier",
    genre="Drama",
    language="English",
    country="USA",
    image="https://m.media-amazon.com/images/M/MV5BOTgyOGQ1NDItNGU3Ny00MjU3LTg2YWEtNmEyYjBiMjI1Y2M5XkEyXkFqcGc@._V1_.jpg"
)
            db.session.add_all([drama1,drama2,drama3,drama4])
            db.session.commit()
        

        if not SciFi.query.first():
            scifi1 = SciFi(
    title="Interstellar",
    year=2014,
    rating=8.7,
    director="Christopher Nolan",
    writer="Jonathan Nolan, Christopher Nolan",
    cast="Matthew McConaughey, Anne Hathaway, Jessica Chastain, Mackenzie Foy, Michael Caine, Matt Damon",
    genre="Sci-Fi",
    language="English",
    country="USA, UK, Canada",
    image="https://cinesnark.com/wp-content/uploads/2014/11/interstellar-poster.jpg?w=620"
)
            scifi2 =  SciFi(
    title="Blade Runner 2049",
    year=2017,
    rating=8.0,
    director="Denis Villeneuve",
    writer="Hampton Fancher, Michael Green, Philip K. Dick",
    cast="Ryan Gosling, Harrison Ford, Ana de Armas, Jared Leto, Robin Wright, Mackenzie Davis",
    genre="Sci-Fi",
    language="English, Finnish, Japanese, Hungarian, Russian, Spanish",
    country="USA, UK, Canada, Hungary, Spain",
    image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNlbNtH-VUeLeM-M7bcZZAm2P3CBd1d3sXIA&s"
)
            scifi3 = SciFi(
    title="The Matrix",
    year=1999,
    rating=8.7,
    director="Lana Wachowski, Lilly Wachowski",
    writer="Lana Wachowski, Lilly Wachowski",
    cast="Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss, Hugo Weaving, Joe Pantoliano, Marcus Chong",
    genre="Sci-Fi",
    language="English",
    country="USA, Australia",
    image="https://th.bing.com/th/id/OIP.BthwaDFzOiwwut5b3y84eQHaK9?rs=1&pid=ImgDetMain"
)
            scifi4 =  SciFi(
    title="Star Wars: A New Hope",
    year=1977,
    rating=8.6,
    director="George Lucas",
    writer="George Lucas",
    cast="Mark Hamill, Harrison Ford, Carrie Fisher, Alec Guinness, Peter Cushing, David Prowse",
    genre="Sci-Fi",
    language="English",
    country="USA",
    image="https://th.bing.com/th/id/OIP.WOsF2BCLWjTxFpUjWM4W5wHaKX?rs=1&pid=ImgDetMain"
)
            db.session.add_all([scifi1, scifi2, scifi3, scifi4])
            db.session.commit()


        if not Horror.query.first():
            horror1 = Horror(
    title="The Conjuring",
    year=2013,
    rating=7.5,
    director="James Wan",
    writer="Chad Hayes, Carey W. Hayes",
    cast="Patrick Wilson, Vera Farmiga, Ron Livingston, Lili Taylor, Shanley Caswell, Hayley McFarland",
    genre="Horror",
    language="English",
    country="USA",
    image="https://images-na.ssl-images-amazon.com/images/S/pv-target-images/792ccf11ad3575bddde05a3105e5e3b32a1725148797ad1c5fe6be8461029b3e._RI_V_TTW_.jpg"
)
            horror2 =  Horror(
    title="Separation",
    year=2021,
    rating=4.7,
    director="William Brent Bell",
    writer="Nick Amadeus, Josh Braun",
    cast="Rupert Friend, Violet McGraw, Madeline Brewer, Mamie Gummer, Brian Cox, Simon Quarterman",
    genre=" Horror",
    language="English",
    country="USA",
    image="https://m.media-amazon.com/images/M/MV5BMmM1OGQwOTUtYWUxZi00ZDRkLTk5MGEtYzYxODBmMWI4M2M1XkEyXkFqcGc@._V1_.jpg"
)          
            horror3 =  Horror(
    title="The Exorcist",
    year=1973,
    rating=8.1,
    director="William Friedkin",
    writer="William Peter Blatty",
    cast="Ellen Burstyn, Max von Sydow, Linda Blair, Lee J. Cobb, Kitty Winn, Jack MacGowran",
    genre="Horror",
    language="English",
    country="USA",
    image="https://image.tmdb.org/t/p/w780/niWzeJeTPXJlHKouGhnoCvhJ3MS.jpg"
)
            horror4 = Horror(
    title="It",
    year=2017,
    rating=7.3,
    director="Andy Muschietti",
    writer="Chase Palmer, Cary Joji Fukunaga, Gary Dauberman, Stephen King (novel)",
    cast="Bill Skarsgård, Jaeden Martell, Finn Wolfhard, Sophia Lillis, Jeremy Ray Taylor, Chosen Jacobs",
    genre="Horror",
    language="English",
    country="USA",
    image="https://m.media-amazon.com/images/M/MV5BZGZmOTZjNzUtOTE4OS00OGM3LWJiNGEtZjk4Yzg2M2Q1YzYxXkEyXkFqcGc@._V1_.jpg"
)
            db.session.add_all([horror1, horror2, horror3, horror4])
            db.session.commit()



            new_user = User(
            name="Admin",
            email="admin@gmail.com",
            mobile=1234567890,
            role="admin"
    )
            new_user.set_password("Admin1234")
            db.session.add(new_user)
            db.session.commit()


    #         new_movie = Action(
    #         title="John Wick",
    #         year=2014,
    #         rating=7.4,
    #         image="https://static1.srcdn.com/wordpress/wp-content/uploads/2024/01/john-wick-franchise-poster.jpg"
    # )
    #         db.session.add(new_movie)
    #         db.session.commit()
            

        # movie = db.session.get(Action, 4)  # Fetch the movie with ID 1 from the Action table
        # if movie:
        #     movie.title = "Avengers Endgame"
        #     movie.year = 2023
        #     movie.rating = 9.0
        #     movie.image = "https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_FMjpg_UX1000_.jpg"
        #     db.session.commit()  # Save changes to the database


setup_db()


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))



@app.route("/login", methods=["GET", "POST"])
def login():


    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")


        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid credentials!", "danger")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():


    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        mobile = request.form.get("mobile")


        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("register"))

        # Check if the email already exists
        if User.query.filter_by(email=email).first():
            flash("Email already exists!", "danger")
            return redirect(url_for("register"))

        if len(password) < 8:
            flash("Password must be at least 8 characters long!", "danger")
            return redirect(url_for("register"))
        
        if not any(char.isupper() for char in password):
            flash("Password must contain at least one uppercase letter!", "danger")
            return redirect(url_for("register"))


        new_user = User(name=name, email=email, mobile=mobile)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()


        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))


    return render_template("/register.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")





@app.route("/about")
def about():
    return render_template("about.html")




@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        logout_user()  # Log the user out
        flash("Logged out successfully!", "info")
        return redirect(url_for('login'))  # Redirect to login page
    return redirect(url_for('login'))



@app.route('/')
def index():
    movies=[
        {'title':'The Dark Knight','year':1996,'rating':9.4,'image':'https://m.media-amazon.com/images/S/pv-target-images/e9a43e647b2ca70e75a3c0af046c4dfdcd712380889779cbdc2c57d94ab63902.jpg'},
        {'title':'Inception','year':1998,'rating':9.3,'image':'https://th.bing.com/th/id/OIP.ps02Cq1ZLtzBEPPpSVttKgHaLH?rs=1&pid=ImgDetMain'},
        {'title':'Barfi','year':1984,'rating':9.7,'image':'https://th.bing.com/th/id/R.14502782cd5dc58bec86aded621c31c6?rik=4aiMWzXin57PMQ&riu=http%3a%2f%2f4.bp.blogspot.com%2f-q3xjcBGBQVA%2fUFIit1azIGI%2fAAAAAAAAgRY%2fFXLXNPFKKbc%2fs1600%2fbarfi_poster.jpg&ehk=snW9hU427Wgyy3xhrQ42IJhsXxveNBmPh%2biVGKfBvWI%3d&risl=&pid=ImgRaw&r=0'},
        {'title':'3 idiots','year':1999,'rating':9.3,'image':'https://th.bing.com/th/id/OIP.qeTgeLDl6ZpMpEaGSff_9AHaJ9?rs=1&pid=ImgDetMain'},
        {'title':'Mufasa: The Lion King','year':1994,'rating':8.3,'image':'https://upload.wikimedia.org/wikipedia/en/thumb/0/0b/Mufasa_The_Lion_King_Movie_2024.jpeg/220px-Mufasa_The_Lion_King_Movie_2024.jpeg'},

    ]
    return render_template('index.html',movies=movies)


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.role != 'admin':
            flash("Access denied!", "danger")
            return redirect(url_for('dashboard'))
        return func(*args, **kwargs)
    return wrapper





@app.route("/add_movie", methods=["POST"])
@login_required
@admin_required
def add_movie():

    
    
    title = request.form.get("title")
    year = request.form.get("year")
    rating = request.form.get("rating")
    image_url = request.form.get("image")
    genre = request.form.get("genre").lower()  # Convert genre input to lowercase

    if not (title and year and rating and image_url and genre):
        return "Missing required fields"

    try:
        year = int(year)
        rating = float(rating)
    except ValueError:
        return "Invalid year or rating"

    # Dictionary to map genres to their respective database models
    genre_map = {
        "action": Action,
        "comedy": Comedy,
        "drama": Drama,
        "scifi": SciFi,
        "horror": Horror,
    }

    if genre in genre_map:
        new_movie = genre_map[genre](title=title, year=year, rating=rating, image=image_url)
        db.session.add(new_movie)
        db.session.commit()
        flash("Movie added successfully!", "success")

    else:
        return "Invalid genre"

    return redirect(url_for("dashboard"))  

@app.route("/update_movie/<genre>/<int:movie_id>", methods=["GET", "POST"])
@login_required
def update_movie(genre, movie_id):
    
    genre_map = {
        "action": Action,
        "comedy": Comedy,
        "drama": Drama,
        "scifi": SciFi,
        "horror": Horror
    }
    
    movie = genre_map[genre.lower()].query.get_or_404(movie_id)
    
    if request.method == "POST":
        movie.title = request.form.get("title")
        movie.year = int(request.form.get("year"))
        movie.rating = float(request.form.get("rating"))
        movie.director = request.form.get("director")
        movie.writer = request.form.get("writer")
        movie.cast = request.form.get("cast")
        movie.language = request.form.get("language")
        movie.country = request.form.get("country")
        movie.description = request.form.get("description")
        movie.image = request.form.get("image")
        db.session.commit()
        flash("Movie updated successfully!", "success")
        return redirect(url_for("dashboard"))
    
    return render_template("update_movie.html", movie=movie, genre=genre)

@app.route("/delete_movie/<genre>/<int:movie_id>", methods=["POST"])
@login_required
@admin_required
def delete_movie(genre, movie_id):
    
    genre_map = {
        "action": Action,
        "comedy": Comedy,
        "drama": Drama,
        "scifi": SciFi,
        "horror": Horror
    }
    
    movie = genre_map[genre.lower()].query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash("Movie deleted successfully!", "success")
    return redirect(url_for("dashboard"))



@app.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        mobile = request.form.get('mobile')

        current_user.name = name
        current_user.email = email
        current_user.mobile = mobile

        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))  


    return render_template('update_profile.html', user=current_user)



@app.route("/dashboard")

def dashboard():
    action_movies = Action.query.all()  
    comedy_movies = Comedy.query.all()  
    drama_movies = Drama.query.all()
    scifi_movies = SciFi.query.all()
    horror_movies = Horror.query.all()
    return render_template("movie.html", action_movies=action_movies, comedy_movies=comedy_movies,drama_movies=drama_movies,scifi_movies=scifi_movies,horror_movies=horror_movies)



@app.route("/movie/<genre>/<int:movie_id>")
def movie_detail(genre, movie_id):
    genre_map = {
        "action": Action,
        "comedy": Comedy,
        "drama": Drama,
        "scifi": SciFi,
        "horror": Horror
    }
    
    movie = genre_map[genre.lower()].query.get_or_404(movie_id)
    return render_template("movie_detail.html", movie=movie, genre=genre)


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if not query:
        return render_template('search_results.html', movies=[], query='')
    
    # Search across all genre tables
    # Adjust this according to your actual model structure
    action_results = Action.query.filter(Action.title.ilike(f'%{query}%')).all()
    comedy_results = Comedy.query.filter(Comedy.title.ilike(f'%{query}%')).all()
    drama_results = Drama.query.filter(Drama.title.ilike(f'%{query}%')).all()
    scifi_results = SciFi.query.filter(SciFi.title.ilike(f'%{query}%')).all()
    horror_results = Horror.query.filter(Horror.title.ilike(f'%{query}%')).all()
    
    # Add genre information to each movie result
    for movie in action_results:
        movie.genre = 'action'
    for movie in comedy_results:
        movie.genre = 'comedy'
    for movie in drama_results:
        movie.genre = 'drama'
    for movie in scifi_results:
        movie.genre = 'scifi'
    for movie in horror_results:
        movie.genre = 'horror'
    
    # Combine all results
    all_results = action_results + comedy_results + drama_results + scifi_results + horror_results
    
    return render_template('search_results.html', movies=all_results, query=query)



api.add_resource(RegisterAPI, '/api/register')
api.add_resource(LoginAPI, '/api/login')
api.add_resource(AddMovieAPI, '/api/add_movie')
api.add_resource(MoviesByGenreAPI, '/api/movies/<string:genre>')
api.add_resource(MovieDetailAPI, "/api/movies/<string:genre>/<int:movie_id>")
api.add_resource(UserInfoAPI, "/api/user_info")
api.add_resource(UpdateProfileAPI, "/api/update_profile")





if __name__ == '__main__':
    app.run(debug=True)