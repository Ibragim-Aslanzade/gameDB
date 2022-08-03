from django.contrib import admin
from .models import Game, Rubric, Profile

class GamesAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'rubric', 'studio', 'rating', 'poster')
    search_fields = ('name', 'studio')

admin.site.register(Game, GamesAdmin)
admin.site.register(Rubric)
admin.site.register(Profile)
