from django.contrib import admin
from movies.models import Movie, MovieStar


class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_date', 'seasons', 'episodes', 'rating']
    search_fields = ['title', 'genre', 'category', 'release_date']


class MovieStarAdmin(admin.ModelAdmin):
    list_display = ['get_movie', 'get_rater', 'stars']
    search_fields = ['movie__title', 'rated_by__username', 'stars']

    list_select_related = ['movie', 'rated_by']


    @admin.display(description='movie title')
    def get_movie(self, obj):
        title = obj.movie.title
        return title
    
    @admin.display(description="rater's username")
    def get_rater(self, obj):
        username = obj.rated_by.username
        return username
    

admin.site.register(Movie, MovieAdmin)
admin.site.register(MovieStar, MovieStarAdmin)
