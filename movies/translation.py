from modeltranslation.translator import register, TranslationOptions
from .models import Category, Author, Book, Genre, BookImage


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Author)
class AuthorTranslationOptions(TranslationOptions):
    fields = ('name', 'biography')


@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Book)
class BookTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(BookImage)
class BookImageTranslationOptions(TranslationOptions):
    fields = ('image',)
