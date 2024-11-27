from django.urls import path

from . import views

urlpatterns = [
    path("", views.BooksView.as_view(), name="home"),
    path("filter/", views.FilterBooksView.as_view(), name='filter'),
    path("search/", views.Search.as_view(), name='search'),
    path("add-rating/", views.AddStarRating.as_view(), name='add_rating'),
    path("json-filter/", views.JsonFilterBooksView.as_view(), name='json_filter'),
    path("<slug:slug>/", views.BookDetailView.as_view(), name="movie_detail"),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
    path("author/<str:slug>/", views.AuthorView.as_view(), name="author_detail"),
    path("category/<int:pk>/", views.CategoryDetailView.as_view(), name="category_detail"),

]

