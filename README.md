# 🎬 MovieDB

MovieDB is a web application similar to IMDb that allows users to browse, search, and view details of movies. It is built with Django (Python), SQLite, and features a responsive frontend.

## 🚀 Features

- 🔍 Search for movies by name
- 🗂️ Browse movies by genre, release year, or rating
- 📄 Detailed movie pages with synopsis, cast, rating, and more
- 📝 Admin panel for adding/editing movies
- 🖼️ Poster/image upload for each movie
- 🎨 Clean and responsive UI

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, Bootstrap 
- **Backend:** Python, Django
- **Database:** SQLite
- **Admin:** Django's built-in admin interface

## 🔧 Installation

1. **Clone the repository**

This repository contains two versions of a Movie Database web application built using:

- **Django** (in `Movie_Database_Django/`)
- **Flask** (in `Movie_Database_Flask/`)

Both applications let users browse and review movies, with user authentication and basic CRUD operations for reviews.



   ```bash
   git clone https://github.com/your-username/movieDb.git
   cd Movie_Database_Django/ or cd Movie_Database_Flask/

Create and activate a virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
Install dependencies

pip install -r requirements.txt

for django:
(
Apply migrations
python manage.py makemigrations
python manage.py migrate
)
Run the server

python manage.py runserver(for django)
python app.py(for flask)

Open in browser
Visit http://127.0.0.1:8000/ to use the app.


📁 Project Structure

G33_MovieDatabase_Repo/
│
├── Movie_Database_Django/
│ ├── MovieDBProject/
│ ├── MovieDBApp/
│ ├── ReviewApp/
│ ├── media/profile_pictures/
│ ├── manage.py
│ └── requirements.txt
│
├── Movie_Database_Flask/
│ ├── models/
│ ├── resource/
│ ├── static/images/
│ ├── templates/
│ ├── app.py
│ ├── app.db
│ └── requirement.txt
│
└── .gitignore



🧠 Future Improvements
User login and registration

User ratings and reviews

API support for external movie data

Pagination and filtering

