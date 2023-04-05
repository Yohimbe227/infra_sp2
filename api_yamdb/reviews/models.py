from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from django.utils import timezone

from api_yamdb.settings import NAME_MAX_LENGTH

User = get_user_model()


class CategoryGenreTitleBase(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)

    class Meta:
        abstract = True
        ordering = ('-id',)

    def __str__(self) -> str:
        return self.name


class ReviewCommentBase(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления',
        db_index=True,
        auto_now_add=True,
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)


class Category(CategoryGenreTitleBase):
    slug = models.SlugField(unique=True)

    class Meta(CategoryGenreTitleBase.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Genre(CategoryGenreTitleBase):
    slug = models.SlugField(unique=True)

    class Meta(CategoryGenreTitleBase.Meta):
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self) -> str:
        return self.name


class Title(CategoryGenreTitleBase):
    description = models.TextField(
        max_length=2000,
        verbose_name='Описание произведения',
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='title',
        blank=True,
        null=True,
        verbose_name='Название категории',
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
    )
    year = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(timezone.now().year),
        ],
    )

    class Meta(CategoryGenreTitleBase.Meta):
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'category', 'year'],
                name='%(app_label)s_%(class)s_unique_relationships',
            ),
        ]


class GenreTitle(models.Model):
    """Auxiliary class GenreTitle for many to many Genre and Title."""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
    verbose_name = 'жанр'


class Review(ReviewCommentBase):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )

    class Meta(ReviewCommentBase.Meta):
        constraints = [
            UniqueConstraint(fields=['author', 'title'], name='review_once'),
        ]


class Comment(ReviewCommentBase):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
