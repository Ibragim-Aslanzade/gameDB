from django import forms
from .models import Game

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

    poster = forms.ImageField(required=True)
    poster.widget.attrs.update({'type': 'file', 'name': 'poster', 'class': "form-control", 'accept':"image/jpeg,image/png"})

    class Meta:
        model = Game
        fields = ['name', 'year', 'description', 'studio', 'rating', 'poster']