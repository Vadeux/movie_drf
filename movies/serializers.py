from rest_framework import serializers

from movies.models import Movie, Category, Actor, Genre, Review


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


class ActorSerializer(serializers.ModelSerializer):
    """Сериализатор для авторов."""

    class Meta:
        model = Actor
        exclude = ('image',)


class MovieListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка фильмов."""
    category = CategorySerializer(read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)
    directors = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('title', 'tagline', 'category', 'genres', 'actors', 'directors',)


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Добавление отзывов."""

    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Вывод отзывов."""

    class Meta:
        model = Review
        fields = ('name', 'text', 'parent', 'email',)


class MovieDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для одного фильма."""
    category = CategorySerializer(read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)
    directors = ActorSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ('draft',)
