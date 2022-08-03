from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponseRedirect
from .models import Game, Rubric, Profile
from .serializer import Game_serializer


def index(request):
    categories = Rubric.objects.all()
    context = {'categories': categories}
    return render(request, 'index.html', context)


def allgames(request):
    # Все категории
    categories = Rubric.objects.all()

    # Поиск
    query = request.GET.get('query')
    if not query:
        query = ""
    game_list = Game.objects.filter(name__icontains=query)

    # Пагинатор
    paginator = Paginator(game_list, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_iterator = paginator.page_range

    context = {'categories': categories, 'games': page_obj, 'pages': page_iterator, 'current_page': page_obj,
               'paginator': paginator, 'query': query}
    return render(request, 'allgames.html', context)


def categories(request):
    categories = Rubric.objects.all()
    context = {'categories': categories}
    return render(request, 'categories.html', context)


def set_category(request, category_id):
    categories = Rubric.objects.all()

    current_category = Rubric.objects.get(pk=category_id)

    # Поиск
    query = request.GET.get('query')
    if not query:
        query = ""
    games = Game.objects.filter(rubric=category_id, name__icontains=query)

    # Пагинатор
    paginator = Paginator(games, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_iterator = paginator.page_range

    context = {'categories': categories, 'current_category': current_category, 'games': page_obj,
               'pages': page_iterator, 'current_page': page_obj, 'paginator': paginator, 'query': query}
    return render(request, 'set_category.html', context)


def detail_page(request, game_id):
    categories = Rubric.objects.all()
    game = Game.objects.get(pk=game_id)
    context = {'categories': categories, 'game': game}
    return render(request, 'detail_page.html', context)


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user and user.is_active:
            auth_login(request, user)

            return redirect('/')

    return render(request, 'registration/login.html')


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR, 'Данный email занят, попробуйте другой')

        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, 'Данный юзернейм занят, попробуйте другой')

        if User.objects.filter(email=email).exists() == False & User.objects.filter(
                username=username).exists() == False:
            User.objects.create_user(
                username=username,
                email=email,
                password=password)

            user = authenticate(username=username, password=password)
            if user and user.is_active:
                auth_login(request, user)

            return redirect('index')

    return render(request, 'registration/register.html')


def logout(request):
    auth_logout(request)
    return render(request, 'registration/logout.html')


class Games_api(APIView):
    def get(self, request, game_id=None):
        # Проверка есть ли game_id
        if game_id == None:
            games = Game.objects.all()
        else:
            games = Game.objects.filter(id=game_id)
        game_serializer = Game_serializer(instance=games, many=True)

        # Проверка правильно ли указан game_id
        if game_serializer.data == []:
            return Response('Игра не найдена')
        else:
            return Response(game_serializer.data)


    def post(self, request):
        serializer = Game_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Запись успешно создана', status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, game_id=None):
        if game_id == None:
            return Response('Нет игры для удаления')
        else:
            game = Game.objects.filter(id=game_id)
            if game.exists():
                game.delete()
                return Response('Игра успешно удалена')
            else:
                return Response('Нет игры для удаления')


def profile(request, user_id):
    categories = Rubric.objects.all()
    profile = Profile.objects.get(user=user_id)

    return render(request, 'profile.html', {'profile': profile, 'categories': categories})

def edit_profile(request):
    categories = Rubric.objects.all()

    name = request.POST.get('name')
    birth = request.POST.get('birth')
    location = request.POST.get('location')
    avatar = request.FILES.get('avatar')
    bio = request.POST.get('bio')


    if name != None and birth != None and location != None and avatar != None and bio != None:
        prof = Profile.objects.get(user=request.user.id)
        prof.name = name
        prof.location = location
        prof.avatar = avatar
        prof.birth_date = birth
        prof.bio = bio
        prof.save()
        return HttpResponseRedirect(f'profile/{request.user.id}')
    else:
        return render(request, 'edit_profile.html', {'categories': categories})


def user_games(request, user_id):
    categories = Rubric.objects.all()

    # Поиск
    query = request.GET.get('query')
    if not query:
        query = ""
    game_list = Game.objects.filter(name__icontains=query, author = user_id)

    # Пагинатор
    paginator = Paginator(game_list, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_iterator = paginator.page_range

    context = {'categories': categories, 'games': page_obj, 'pages': page_iterator, 'current_page': page_obj,
               'paginator': paginator, 'query': query}

    return render(request, 'user_games.html', context)

def add_game(request):
    categories = Rubric.objects.all()

    name = request.POST.get('name')
    year = request.POST.get('year')
    studio = request.POST.get('studio')
    poster = request.FILES.get('poster')
    description = request.POST.get('description')
    rating = request.POST.get('rating')
    category = request.POST.get('category')

    if name != None and year != None and studio != None and poster != None and description != None and rating != None:
        category_db = Rubric.objects.get(name=category)
        game = Game.objects.create(name=name, year=year, description=description, studio=studio, rating=rating, poster=poster, rubric=category_db, author=request.user)

        return HttpResponseRedirect(reverse('detail_page', kwargs={'game_id': game.id}))
    else:
        return render(request, 'add_game.html', {'categories': categories})