from django.urls import path

from . import views

urlpatterns = [
    path('movie/', views.MovieListView.as_view(), name='movie_list'),
    path('movie/<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('review/', views.ReviewCreateView.as_view(), name='create_review'),
    path('rating/', views.AddStarRatingView.as_view(), name='create_rating'),
    path('actors/', views.ActorListView.as_view(), name='actors_list'),
    path('actors/<int:pk>/', views.ActorDetailView.as_view(), name='actor_detail'),
]
