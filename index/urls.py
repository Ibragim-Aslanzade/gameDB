from django.urls import path, include
from .views import index, allgames, categories,set_category, detail_page, register, login, Games_api, logout, profile,  edit_profile, user_games, add_game

urlpatterns = [
    path('', index, name='index'),
    path('allgames/', allgames, name='allgames'),
    path('categories/', categories, name='categories'),
    path('categories/<int:category_id>', set_category, name='set_category'),
    path('allgames/<int:game_id>', detail_page, name='detail_page'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('games_api/' ,Games_api.as_view()),
    path('games_api/<int:game_id>' ,Games_api.as_view()),
    path('profile/<int:user_id>', profile, name='profile'),
    path('edit_profile', edit_profile, name='edit_profile'),
    path('profile/<int:user_id>/games/', user_games, name='user_games'),
    path('add_game/', add_game, name='add_game')
]