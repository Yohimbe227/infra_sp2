from django_filters import CharFilter
from django_filters.rest_framework import FilterSet

from reviews.models import Title


class TitleFilter(FilterSet):
    """
    The custom filter.

    Filtering fields `slug` as `genre`,`slug` as `category`,
    `year` and `name` as is in `Title` model.
    `slug` is the field from `Genre` model.
    `slug` is the field from `Category` model.
    """

    genre = CharFilter(
        field_name='genre__slug',
    )
    category = CharFilter(field_name='category__slug')

    class Meta:
        model = Title
        fields = ['genre', 'category', 'year', 'name']
