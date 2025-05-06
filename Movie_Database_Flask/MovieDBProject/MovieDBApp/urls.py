from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/remove-favorite/<int:movie_id>/', views.remove_favorite, name='remove_favorite'),
    path('logout/', views.logout_view, name='logout'),
    # path('movie/', views.movie_list, name='movie'),
    # path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('add-to-favorites/<int:movie_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('search/', views.search_movie, name='search_movie'),
    path('movie/add/', views.add_movie, name='add_movie'),
    path('movie/<int:movie_id>/edit/', views.edit_movie, name='edit_movie'),
    path('movie/<int:movie_id>/delete/', views.delete_movie, name='delete_movie'),
    path('movie/',views.movie_list,name='movie'),
    path('movie/<str:title>/', views.movie_detail, name='movie_detail'),
    path('genre/<str:genre_name>/', views.genre_all_movies, name='genre_all_movies'),
    path('search/json/', views.search_movie_json, name='search_movie_json'),
]