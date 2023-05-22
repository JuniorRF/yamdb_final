import datetime as dt

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class TokenSerializer(serializers.Serializer):
    """Сериализатор для выдачи пользователю Токена."""
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=150,
        required=True
    )


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации."""
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )

    email = serializers.EmailField(
        max_length=254,
        required=True
    )

    class Meta:
        fields = ('username', 'email', )

    def validate(self, data):
        """Запрет на имя me, А так же Уникальность полей username и email."""
        if data.get('username').lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя me запрещено'
            )
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_username(self, username):
        if username.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя me запрещено'
            )
        return username


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор Для Комментариев."""
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор класса Category."""
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор класса Genre."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate_score(self, value):
        if 0 > value or value > 10:
            raise serializers.ValidationError('Оценка по 10-бальной шкале!')
        return value

    def validate(self, data):
        request = self.context['request']
        current_user = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title,
                                      author=current_user).exists()
        ):
            raise ValidationError('Может существовать только один отзыв!')
        return data

    class Meta:
        fields = '__all__'
        model = Review


class TitleGETSerializer(serializers.ModelSerializer):
    """Сериализатор класса Title при GET запросах."""

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор класса Title при остальных запросах."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'name',
            'year',
            'description',
            'genre',
            'category'
        )

    def validate_year(self, value):
        current_year = dt.datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                'Неправильная дата: год не может быть больше текущего.'
            )
        return value

    def to_representation(self, title):
        serializer = TitleGETSerializer(title)
        return serializer.data


class ReadTitleSerializer(serializers.ModelSerializer):
    """Сериализатор Для чтения произведений."""
    description = serializers.CharField(required=False)
    genre = GenreSerializer(many=True)
    category = CategorySerializer(required=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'
