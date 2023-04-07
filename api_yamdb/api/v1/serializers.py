from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )


class TitleWriteSerializer(serializers.ModelSerializer):

    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all(),
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    rating = serializers.IntegerField(read_only=True)

    def validate_year(self, year: int) -> int:
        """Проверка даты.

        Args:
            year: Год создания произведения (указывает пользователь).

        Returns:
            Год создания произведения (проверено).

        Raises:
             ValidationError: Введите корректный год!
        """
        if year > timezone.now().year:
            raise serializers.ValidationError('Введите корректный год!')
        return year

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'category',
            'genre',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=['name', 'category', 'year'],
                message='Это произведение уже добавлено!',
            ),
        ]


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(
        read_only=True,
        many=True,
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'category',
            'genre',
        )


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        user = self.context['request'].user
        title_id = self.context['request'].parser_context['kwargs']['title_id']
        if Review.objects.filter(author=user, title__id=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на данное произведение!'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )


class RegistrationSerializer(serializers.Serializer):

    username = serializers.CharField(
        max_length=settings.USERNAME_MAX_LENGTH, required=True
    )
    email = serializers.EmailField(
        max_length=settings.AUTH_MAX_LENGTH,
        required=True,
    )

    def validate_username(self, value):
        if value in settings.BANNED_WORDS:
            raise serializers.ValidationError("Can't use username 'me'!")
        validate_symbols = UnicodeUsernameValidator()
        validate_symbols.__call__(value)
        return value

    def filter_data(self, data):
        if User.objects.filter(email__exact=data.get('email')).exists():
            raise serializers.ValidationError("Mistake in field username!")
        if User.objects.filter(username__exact=data.get('username')).exists():
            raise serializers.ValidationError("Mistake in field email!")
        return data


class TokenObtainSerializer(serializers.Serializer):

    username = serializers.CharField(
        max_length=settings.USERNAME_MAX_LENGTH,
        required=True,
    )
    confirmation_code = serializers.CharField(
        max_length=settings.AUTH_MAX_LENGTH,
        required=True,
    )

    def filter_confirmation_code(self, user, value):
        if user.confirmation_code != value:
            raise serializers.ValidationError("Mistake in field email!")
        return value


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class CustomUserSerializer(AdminSerializer):
    class Meta(AdminSerializer.Meta):
        read_only_fields = ('role',)
