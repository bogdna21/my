from django.db import models

from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва категорії")
    description = models.TextField(verbose_name="Опис", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Author(models.Model):
    name = models.CharField(max_length=255, verbose_name="Ім'я автора")
    biography = models.TextField(verbose_name="Біографія", blank=True, null=True)
    photo = models.ImageField(upload_to='authors/', verbose_name="Фото", blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={"slug": self.name})

    class Meta:
        verbose_name = "Актеры и режиссеры"
        verbose_name_plural = "Актеры и режиссеры"


class Genre(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва жанру")

    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанри"


class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name="Назва книги")
    author = models.ManyToManyField('Author', verbose_name="Автори")
    description = models.TextField(verbose_name="Опис")
    genre = models.ManyToManyField('Genre', verbose_name="Жанри")
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, verbose_name="Категорія")
    cover_image = models.ImageField(upload_to='covers/', verbose_name="Обкладинка", blank=True, null=True)
    pdf_file = models.FileField(upload_to='books/', verbose_name="Файл книги", blank=True, null=True)
    external_link = models.URLField(verbose_name="Посилання", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    draft = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_detail", kwargs={"pk": self.pk})

    def get_review(self):
        return self.reviews.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"


class BookImage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="images", verbose_name="Книга")
    image = models.ImageField(upload_to='book_images/', verbose_name="Ілюстрація")

    def __str__(self):
        return self.book.title
    class Meta:
        verbose_name = "Кадр из фильма"
        verbose_name_plural = "Кадры из фильма"


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="ratings", verbose_name="Книга", default=1)
    user = models.CharField(max_length=255, verbose_name="Користувач", default="Unknown User")
    value = models.PositiveSmallIntegerField(default=1, verbose_name="Оцінка")

    def __str__(self):
        return f"{self.value} - {self.book.title}"


    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews", verbose_name="Книга")
    user = models.CharField(max_length=255, verbose_name="Користувач")
    text = models.TextField(verbose_name="Текст відгуку")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    def __str__(self):
        return f"{self.user} - {self.book.title}"


    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
