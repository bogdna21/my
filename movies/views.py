from django.db import models
from django.http import Http404
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Book, Category, Author, Genre, Rating, Review
from .forms import ReviewForm, RatingForm


class GenreYear:
    """Жанри і роки публікації книг"""

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Book.objects.filter(draft=False).values("year")


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class BooksView(GenreYear, ListView):
    """Список книг"""
    model = Book
    queryset = Book.objects.filter(draft=False).order_by('id')
    paginate_by = 3
    template_name = "movies/movie_list.html"
    context_object_name = 'book_list'

    def get(self, request, *args, **kwargs):
        print(f"Запит URL: {request.path}")
        return super().get(request, *args, **kwargs)


class BookDetailView(DetailView):
    model = Book
    template_name = 'movies/movie_detail.html'
    context_object_name = 'book'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get(self, request, *args, **kwargs):
        print(f"Slug: {kwargs.get('slug')}")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("Контекст:", context)
        return context


class AddReview(View):
    """Відгуки про книгу"""

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        book = Book.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.book = book
            form.save()
        return redirect(book.get_absolute_url())


class AuthorView(GenreYear, DetailView):
    """Інформація про автора"""
    model = Author
    template_name = 'movies/actor.html'
    slug_field = "name"


class FilterBooksView(GenreYear, ListView):
    """Фільтр книг"""
    paginate_by = 3
    template_name = "movies/movie_list.html"

    def get_queryset(self):
        queryset = Book.objects.all()

        years = self.request.GET.getlist("year")
        if years:
            queryset = queryset.filter(year__in=years)

        genres = self.request.GET.getlist("genre")
        if genres:
            queryset = queryset.filter(genre__in=genres)

        return queryset.distinct()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
        context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
        return context


class JsonFilterBooksView(ListView):
    """Фільтрація книг у форматі JSON"""

    def get_queryset(self):
        queryset = Book.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genre__in=self.request.GET.getlist("genre"))
        ).distinct().values("title", "tagline", "url", "cover_image")
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"books": queryset}, safe=False)


class AddStarRating(View):
    """Оцінка книги"""

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                book_id=int(request.POST.get("book")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class Search(ListView):
    """Пошук книг"""
    paginate_by = 3

    def get_queryset(self):
        return Book.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = "include/header.html"  # Шаблон для категорії
    context_object_name = "category"