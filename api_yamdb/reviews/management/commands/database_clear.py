from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title

User = get_user_model()


class Command(BaseCommand):
    """
    Database clearing.
    """

    def handle(self, *args, **options) -> None:
        """
        Handler for the management command `database_clear`.

        Args:
            *args: not used.
            **options: not used.

        Returns:
            None.
        """
        Genre.objects.all().delete()
        Title.objects.all().delete()
        Category.objects.all().delete()
        GenreTitle.objects.all().delete()
        User.objects.all().delete()
        Comment.objects.all().delete()
        Review.objects.all().delete()
