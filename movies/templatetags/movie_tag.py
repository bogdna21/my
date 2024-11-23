from django import template
from movies.models import Category, Book

register = template.Library()


@register.simple_tag()
def get_categories():
    """Вивід усіх категорій"""
    return Category.objects.all()


@register.inclusion_tag('movies/tags/last_movie.html')
def get_last_books(count=5):
    books = Book.objects.order_by("id")[:count]
    return {"last_books": books}
