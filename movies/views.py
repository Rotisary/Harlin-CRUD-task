from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from django.db.models import Q

from movies.models import Movie, MovieStar
from users.decorators import login_required, email_verif_required


@method_decorator([login_required(), email_verif_required()], name="dispatch")
class AddMovieView(CreateView):
    model = Movie
    fields = ['title', 'star_actors', 'category', 'genre', 'release_date', 'seasons', 'episodes']


    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)


@method_decorator([login_required(), email_verif_required()], name="dispatch")
class MovieDetailView(DetailView):
    model = Movie
    context_object_name = 'movie'


    def get_object(self, queryset=None):
        title = self.kwargs.get('title')
        pk = self.kwargs.get('pk')
        return get_object_or_404(Movie, title__iexact=title, id=pk)


@method_decorator([login_required(), email_verif_required()], name="dispatch")
class MovieUpdateView(UserPassesTestMixin, UpdateView):
    model = Movie
    fields = ['title', 'star_actors', 'category', 'genre', 'release_date', 'seasons', 'episodes']


    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)


    def test_func(self):
        movie = self.get_object()
        if self.request.user == movie.posted_by:
            return True
        else:
            return False


@method_decorator([login_required(), email_verif_required()], name="dispatch")
class MovieDeleteView(UserPassesTestMixin, DeleteView):
    model = Movie
    context_object_name = 'movie'
    success_url = reverse_lazy('movies-list') 


    def test_func(self):
        movie = self.get_object()
        if self.request.user == movie.posted_by:
            return True
        else:
            return False


@method_decorator([login_required(), email_verif_required()], name="dispatch")
class MoviesListView(ListView):
    models = Movie
    template_name = 'movies/movies_list.html'
    context_object_name = 'movies'
    ordering = '-posted_on'
    paginate_by = 5


    def get_queryset(self):
        category = self.request.GET.get('category')
        genre = self.request.GET.get('genre')
        search = self.request.GET.get('search')
        list = [] 
        # filter movies by catgory
        if category:        
            for movie in Movie.objects.all().order_by('-posted_on'):
                if category.upper() in movie.category:
                    list.append(movie)
        # filter movies by genre 
        elif genre:       
            for movie in Movie.objects.all().order_by('-posted_on'):
                if genre.upper() in movie.genre:
                    list.append(movie)
        elif search:
            list = Movie.objects.filter(Q(title__icontains=search) | Q(star_actors__icontains=search)).order_by('-posted_on')
        # return all movies if there is no filter           
        else: 
            list = Movie.objects.all().order_by('-posted_on')
        return list


@login_required()
@email_verif_required()
def rate_movie(request, title, pk):
    movie = Movie.objects.get(title__iexact=title, id=pk)
    if request.method == "POST":
        stars = int(request.POST.get('rating', 0))
        if MovieStar.objects.filter(movie=movie, rated_by=request.user).exists():
            messages.info(request, 'you have already rated this movie')
            HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            if stars >= 1 and stars <= 5: 
                movie_rating = MovieStar.objects.create(stars=stars,
                                                        movie=movie,
                                                        rated_by=request.user)
                movie_rating.save()

                # update movie's rating
                ratings_of_movie = movie.ratings.all()
                sum_of_stars = 0
                for rating in ratings_of_movie:
                    sum_of_stars += rating.stars
                try:
                    computed_rating = sum_of_stars/ratings_of_movie.count()
                    movie.rating = round(computed_rating, 1)
                    movie.save()
                except ZeroDivisionError:
                    movie.rating = 0
                return HttpResponseRedirect(reverse('movie-detail', kwargs={'title': movie.title, 'pk': movie.id}))
            else:
                messages.info(request, 'your rating cannot be 0')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
  
    context = {'movie': movie}
    return render(request, 'movies/rate_movie.html', context)


