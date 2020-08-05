from rest_framework import serializers

from movies.models import Movie, Category, Actor, Genre, Review, Rating


class FilterReviewListSerializer(serializers.ListSerializer):
    """Фильтр комментариев типа parent."""

    def to_representation(self, data):  # data = queryset
        data = data.filter(parent=None)
        return super(FilterReviewListSerializer, self).to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Рекурсивный вывод детей отзывов."""

    def to_representation(self, value):  # value - значение одной записи из базы данных
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Category
        fields = ('name', 'description', 'url',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'description', 'url',)


class ActorListSerializer(serializers.ModelSerializer):
    """Сериализатор для актеров и режиссеров."""

    class Meta:
        model = Actor
        fields = ('id', 'name', 'image',)


class ActorDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для актеров и режиссеров."""

    class Meta:
        model = Actor
        fields = '__all__'


class MovieListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка фильмов."""
    category = CategorySerializer(read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorListSerializer(many=True, read_only=True)
    directors = ActorListSerializer(many=True, read_only=True)
    rating_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()

    class Meta:
        model = Movie
        fields = ('id', 'title', 'tagline', 'category', 'genres', 'actors', 'directors', 'rating_user', 'middle_star',)


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Добавление отзывов."""

    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Вывод отзывов."""
    # Для создания отступа уровень дочерний.
    children = RecursiveSerializer(many=True)

    class Meta:
        # Для того, чтобы удалить отзывы без родителя из отступа родителей.
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ('name', 'text', 'email', 'children',)


class MovieDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для одного фильма."""
    category = CategorySerializer(read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorListSerializer(many=True, read_only=True)
    directors = ActorListSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ('draft',)


class CrateRatingSerializer(serializers.ModelSerializer):
    """Оценка (выставление рейтинга) фильмам."""

    class Meta:
        model = Rating
        fields = ('star', 'movie',)

    def create(self, validated_data):  # Для того чтобы обновлялась запись, а не создавалась новая
        rating, _ = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get('star')}  # Поле которое мы будем обновлять (star)
        )
        return rating
