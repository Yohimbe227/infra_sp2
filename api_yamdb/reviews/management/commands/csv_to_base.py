import csv
from pathlib import Path
from typing import List

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User


def path_become(file_name: str) -> Path:
    return Path(settings.CSV_DATA_DIR, file_name)


class Command(BaseCommand):
    # order is really important!
    files_to_models = (
        ('category.csv', Category),
        ('genre.csv', Genre),
        ('users.csv', User),
        ('titles.csv', Title),
        ('review.csv', Review),
        ('genre_title.csv', GenreTitle),
        ('comments.csv', Comment),
    )

    def check_files(self) -> None:
        """
        Folder presence check.

        Сheck for each file in the tuple `files_to_models`.
        Returns:
           None.

        Raises:
            FileNotFoundError: Файл не найден.
        """

        for file_name, _ in self.files_to_models:
            if not path_become(file_name).is_file():
                raise FileNotFoundError(f'{file_name} not exist')

    def to_base(self):
        """
        Transfer data from csv files in the `static/data` directory
        to the database. The names of the columns in the files and fields
        in the corresponding models must match.
        Returns:
            None.
        """
        for file_name, model in self.files_to_models:
            file: Path = path_become(file_name)
            date_list = []
            with open(file, 'r', encoding='utf8') as csv_file:
                reader = csv.reader(csv_file, delimiter=',', quotechar='"')
                for num, row in enumerate(reader):
                    if not num:
                        header: List[str] = row
                        continue
                    for index, param in enumerate(header):
                        if param == 'category' or param == 'author':
                            header[index] += '_id'
                    new_date = model(
                        **{key: value for key, value in zip(header, row)},
                    )
                    date_list.append(new_date)
                model.objects.bulk_create(date_list, ignore_conflicts=True)

    def handle(self, *args, **options) -> None:
        """
        Handler for the management command `csv_to_base`.

        Args:
            *args: not used.
            **options: not used.

        Returns:
            None.
        """
        del args, options
        self.check_files()
        self.to_base()
