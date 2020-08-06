from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models

from .models import Movie, Actor
from .serializers import MovieListSerializer, \
    MovieDetailSerializer, \
    ReviewCreateSerializer, \
    CrateRatingSerializer, \
    ActorListSerializer, \
    ActorDetailSerializer
from .service import get_client_ip, MovieFilter


class MovieListView(generics.ListAPIView):
    """Список фильмов."""

    serializer_class = MovieListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter  # Фильтр, который будет фильтровать записи по url/?year_min=...
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies


class MovieDetailView(generics.RetrieveAPIView):
    """Отдельный фильм."""
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer


class ReviewCreateView(generics.CreateAPIView):
    """Добавление отзыва к фильму."""
    serializer_class = ReviewCreateSerializer


class AddStarRatingView(generics.CreateAPIView):
    """Добавление рейтинга к фильму."""
    serializer_class = CrateRatingSerializer

    def perform_create(self, serializer):  # Для каких-либо действий при сохранении.
        serializer.save(ip=get_client_ip(self.request))


class ActorListView(generics.ListAPIView):
    """Вывод всех актеров и режисеров."""
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(generics.RetrieveAPIView):
    """Вывод информации об одном актере или режиссере."""
    queryset = Actor.objects.all()  # use lookup_fields='field' to search 1 obj (not by pk!)
    serializer_class = ActorDetailSerializer
