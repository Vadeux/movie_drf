from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models

from .models import Movie, Actor
from .serializers import MovieListSerializer, \
    MovieDetailSerializer, \
    ReviewCreateSerializer, \
    CreateRatingSerializer, \
    ActorListSerializer, \
    ActorDetailSerializer
from .service import get_client_ip, MovieFilter, PaginationMovies


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод списка или одного фильма"""
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    pagination_class = PaginationMovies

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings",
                                     filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        elif self.action == "retrieve":
            return MovieDetailSerializer


class ReviewCreateViewSet(viewsets.ModelViewSet):
    """Добавление отзыва к фильму"""
    serializer_class = ReviewCreateSerializer


class AddStarRatingViewSet(viewsets.ModelViewSet):
    """Добавление рейтинга фильму"""
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод актеров или режиссеров"""
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorListSerializer
        elif self.action == "retrieve":
            return ActorDetailSerializer

# class MovieListView(generics.ListAPIView):
#     """Список фильмов."""
#
#     serializer_class = MovieListSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = MovieFilter  # Фильтр, который будет фильтровать записи по url/?year_min=...
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_queryset(self):
#         movies = Movie.objects.filter(draft=False).annotate(
#             rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
#         ).annotate(
#             middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
#         )
#         return movies
#
#
# class MovieDetailView(generics.RetrieveAPIView):
#     """Отдельный фильм."""
#     queryset = Movie.objects.filter(draft=False)
#     serializer_class = MovieDetailSerializer
#
#
# class ReviewCreateView(generics.CreateAPIView):
#     """Добавление отзыва к фильму."""
#     serializer_class = ReviewCreateSerializer
#
#
# class AddStarRatingView(generics.CreateAPIView):
#     """Добавление рейтинга к фильму."""
#     serializer_class = CrateRatingSerializer
#
#     def perform_create(self, serializer):  # Для каких-либо действий при сохранении.
#         serializer.save(ip=get_client_ip(self.request))
#
#
# class ActorListView(generics.ListAPIView):
#     """Вывод всех актеров и режисеров."""
#     queryset = Actor.objects.all()
#     serializer_class = ActorListSerializer
#
#
# class ActorDetailView(generics.RetrieveAPIView):
#     """Вывод информации об одном актере или режиссере."""
#     queryset = Actor.objects.all()  # use lookup_fields='field' to search 1 obj (not by pk!)
#     serializer_class = ActorDetailSerializer
