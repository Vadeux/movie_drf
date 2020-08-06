from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views, api

urlpatterns = format_suffix_patterns([
    path('movie/', views.MovieViewSet.as_view({'get': 'list'}), name='movie_list'),
    path('movie/<int:pk>/', views.MovieViewSet.as_view({'get': 'retrieve'}), name='movie_detail'),
    path('review/', views.ReviewCreateViewSet.as_view({'post': 'create'}), name='create_review'),
    path('rating/', views.AddStarRatingViewSet.as_view({'post': 'create'}), name='create_rating'),
    path('actor/', views.ActorsViewSet.as_view({'get': 'list'})),  # key - http-method, val - function
    path('actor/<int:pk>/', views.ActorsViewSet.as_view({'get': 'retrieve'})),
])

# urlpatterns = [
#     path('movie/', views.MovieListView.as_view(), name='movie_list'),
#     path('movie/<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
#     path('review/', views.ReviewCreateView.as_view(), name='create_review'),
#     path('rating/', views.AddStarRatingView.as_view(), name='create_rating'),
#     path('actors/', views.ActorListView.as_view(), name='actors_list'),
#     path('actors/<int:pk>/', views.ActorDetailView.as_view(), name='actor_detail'),
#     path('actor/', api.ActorViewSet.as_view({'get': 'list'})),  # key - http-method, val - function
#     path('actor/<int:pk>/', api.ActorViewSet.as_view({'get': 'retrieve'})),
# ]
