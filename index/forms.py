from django import forms
from .models import Game, Rubric
from django.contrib.auth.models import User

class GameForm(forms.ModelForm):
    name = forms.CharField(required=True)
    name.widget.attrs.update({'type': 'text', 'name': 'name', 'class': "form-control"})

    year = forms.IntegerField(required=True)
    year.widget.attrs.update({'type': 'number', 'name': 'year', 'class': "form-control"})

    description = forms.CharField(required=True)
    description.widget.attrs.update({'type': 'text', 'name': 'description', 'class': "form-control"})

    studio = forms.CharField(required=True)
    studio.widget.attrs.update({'type': 'text', 'name': 'studio', 'class': "form-control"})

    rating = forms.IntegerField(required=True)
    rating.widget.attrs.update({'type': 'number', 'name': 'rating', 'class': "form-control"})

    rubric = forms.ModelChoiceField(required=True, queryset=Rubric.objects.all(), empty_label='Выберите категорию')
    rubric.widget.attrs.update({'class':"form-control", 'name':"category"})

    poster = forms.ImageField(required=True)
    poster.widget.attrs.update({'type': 'file', 'name': 'poster', 'class': "form-control", 'accept':"image/jpeg,image/png"})

    class Meta:
        model = Game
        fields = ['name', 'year', 'description', 'studio', 'rating', 'poster', 'rubric']

class UserForm(forms.ModelForm):
    username = forms.CharField(required=True)
    username.widget.attrs.update({'class': "form-control", 'name': "username", 'minlength': '6'})

    email = forms.CharField(required=True, widget=forms.EmailInput)
    email.widget.attrs.update({'class': "form-control", 'name': "email"})

    password = forms.CharField(required=True, widget=forms.PasswordInput)
    password.widget.attrs.update({'class': "form-control", 'name': "password", 'minlength': '8'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password']