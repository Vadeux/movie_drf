from django.urls import path

from . import views

urlpatterns = [
    path('movie/', views.MovieListView.as_view(), name='movie_list'),
    path('movie/<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('review/', views.ReviewCreateView.as_view(), name='create_review'),
]
