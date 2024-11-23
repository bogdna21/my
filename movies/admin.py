from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Book, Category, Genre, Author, Review


class BookAdminForm(forms.ModelForm):
    """Форма для книги з CKEditor"""
    description = forms.CharField(label="Опис", widget=CKEditorUploadingWidget())
    description_en = forms.CharField(label="Description", widget=CKEditorUploadingWidget())

    class Meta:
        model = Book
        fields = '__all__'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    form = BookAdminForm
    list_display = ('title', 'get_authors', 'category', 'created_at')  # Замінено author на get_authors
    search_fields = ('title', 'author__name')
    list_filter = ('category', 'genre')
    filter_horizontal = ('genre', 'author')

    def get_authors(self, obj):
        return ", ".join([author.name for author in obj.author.all()])
    get_authors.short_description = "Автори"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'created_at')
    search_fields = ('book__title', 'user')

