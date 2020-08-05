from django_filters import rest_framework as filters
from movies.models import Movie


def get_client_ip(request):
    """Получение IP пользователя."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):  # Т.к. in в поиске, и жанр по имени,а не по id
    pass


class MovieFilter(filters.FilterSet):
    genres = CharFilterInFilter(field_name='genres__name', lookup_expr='in')
    year = filters.RangeFilter()  # Диаразон в урле year_min=| year_max=

    class Meta:
        model = Movie
        fields = ['genres', 'year']
