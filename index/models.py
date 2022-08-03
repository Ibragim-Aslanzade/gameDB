from django.db import models
from cloudinary.models import CloudinaryField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Profile(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=50, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = CloudinaryField(blank=True, null=True, verbose_name='Аватар')
    bio = models.TextField(max_length=500, blank=True, null=True, verbose_name='Био')
    location = models.CharField(max_length=30, blank=True, null=True, verbose_name='Страна')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name='Профиль'
        verbose_name_plural = 'Профили'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Game(models.Model):
    name = models.CharField(verbose_name='Название', max_length=300)
    year = models.IntegerField(verbose_name='Год выхода')
    description = models.TextField(verbose_name='Описание', max_length=10000)
    studio = models.CharField(verbose_name='Разработчик', max_length=300)
    rating = models.FloatField(verbose_name='Рейтинг')
    poster = CloudinaryField('poster')
    rubric = models.ForeignKey(verbose_name='Рубрика', to='Rubric', on_delete=models.PROTECT)
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = "Игры"
        ordering = ['id']

class Rubric(models.Model):
    name = models.CharField(verbose_name='Название', max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'
