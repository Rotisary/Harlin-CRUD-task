from django.db import models
from django.conf import settings
from django.urls import reverse
from django.template.defaultfilters import slugify

from multiselectfield import MultiSelectField


class Movie(models.Model):
    MOVIE_CATEGORIES = [
        ('MOVIE', 'Movie'),
        ('TV_SHOW', 'TV Show'),
        ('SERIES', 'series'),
        ('ANIMATION', 'animation'),
        ('CARTOON', 'cartoon'),
        ('ANIME', 'anime')
    ]
    GENRE_CHOICES = [
        ('ACTION', 'action'),
        ('COMEDY', 'comedy'),
        ('THRILLER', 'thriller'),
        ('DRAMA', 'drama'),
        ('TRAGEDY', 'tragedy'),
        ('HORROR', 'horror'),
        ('SCI_FI', 'sci-fi'),
        ('FANTASY', 'fantasy'),
        ('ROMANCE', 'romance'),
        ('MUSICAL','musical'),
    ]
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  related_name='posted_movies',
                                  on_delete=models.CASCADE,
                                  null=False,
                                  blank=False)
    title = models.CharField(max_length=225,
                             null=False,
                             blank=False)
    star_actors = models.CharField(max_length=250,
                                   blank=False,
                                   null=False)
    category = MultiSelectField(choices=MOVIE_CATEGORIES, 
                                max_choices=6, 
                                max_length=100,
                                blank=False,
                                null=False)
    genre = MultiSelectField(choices=GENRE_CHOICES, 
                            max_choices=10, 
                            max_length=100,
                            blank=False,
                            null=False)
    release_date = models.DateField(blank=False, null=False)
    seasons = models.IntegerField(default=0, null=True, blank=True)
    episodes = models.IntegerField(default=0, null=True, blank=True)
    rating = models.FloatField(default=0, null=False, blank=False)
    posted_on = models.DateTimeField(auto_now_add=True, blank=False, null=False)


    def __str__(self):
        return f"{self.title}"
    

    def get_absolute_url(self):
        return reverse('movie-detail', kwargs={'title': self.title, 'pk': self.pk})
    


class MovieStar(models.Model):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    STARS = [
        (ONE, 1),
        (TWO, 2),
        (THREE, 3),
        (FOUR, 4),
        (FIVE, 5)
    ]
    stars = models.IntegerField(choices=STARS, null=False, blank=False)
    movie = models.ForeignKey(Movie, 
                              related_name='ratings',
                              null=False,
                              blank=False,
                              on_delete=models.CASCADE)
    rated_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 related_name='ratings_dropped',
                                 null=False,
                                 blank=False,
                                 on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(auto_now_add=True, blank=False, null=False)


    def __str__(self):
        return f"{self.movie.title}'s rating-{self.id}"
