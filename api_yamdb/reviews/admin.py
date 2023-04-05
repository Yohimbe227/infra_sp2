from django.contrib import admin

from reviews.models import Category, Genre, GenreTitle, Title


class BaseAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'


class GenreTitleInline(admin.TabularInline):
    model = GenreTitle
    extra = 1


@admin.register(Genre)
class GenreAdmin(BaseAdmin):
    model = Genre
    inlines = [
        GenreTitleInline,
    ]
    list_display = (
        'pk',
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('slug',)


@admin.register(Title)
class TitleAdmin(BaseAdmin):
    inlines = [
        GenreTitleInline,
    ]
    list_display = (
        'pk',
        'name',
        'category',
    )
    list_editable = ('category',)
    search_fields = (
        'name',
        'category',
    )
    list_filter = (
        'genre',
        'category',
    )


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('slug',)
