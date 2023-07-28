import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from reviews.models import Category, Comment, Genre, Review, Title, User


class Command(BaseCommand):
    help = 'Выполнить импорт данных из csv файла'

    def handle(self, *args, **kwargs):
        file_path = settings.STATICFILES_DIRS[0] / 'data' / 'category.csv'
        with open(file_path, encoding='utf-8') as csv_file:
            reader_object = csv.reader(csv_file)
            next(reader_object)
            for row in reader_object:
                obj, created = Category.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                )
            print('Данные категорий загружены в БД!')
        file_path = settings.STATICFILES_DIRS[0] / 'data' / 'genre.csv'
        with open(file_path, encoding='utf-8') as csv_file:
            reader_object = csv.reader(csv_file)
            next(reader_object)
            for row in reader_object:
                obj, created = Genre.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                )
            print('Данные жанров загружены в БД!')
        file_path = settings.STATICFILES_DIRS[0] / 'data' / 'titles.csv'
        with open(file_path, encoding='utf-8') as csv_file:
            reader_object = csv.reader(csv_file)
            next(reader_object)
            for row in reader_object:
                obj, created = Title.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    year=row[2],
                    category_id=row[3],
                )
            print('Данные произведений загружены в БД!')
        file_path = settings.STATICFILES_DIRS[0] / 'data' / 'genre_title.csv'
        with open(file_path, encoding='utf-8') as csv_file:
            reader_object = csv.reader(csv_file)
            next(reader_object)
            for row in reader_object:
                genre_list = []
                obj_genre = get_object_or_404(Genre, id=row[2])
                genre_list.append(obj_genre)
                obj, created = Title.objects.get_or_create(
                    id=row[1],
                )
                try:
                    genre_list.append(obj.genre.get())
                except Exception:
                    pass
                obj.genre.set(genre_list)
            print('Данные жанров произведений загружены в БД!')
        file_path = settings.STATICFILES_DIRS[0] / 'data' / 'users.csv'
        with open(file_path, encoding='utf-8') as csv_file:
            reader_object = csv.reader(csv_file)
            next(reader_object)
            for row in reader_object:
                obj, created = User.objects.get_or_create(
                    id=row[0],
                    username=row[1],
                    email=row[2],
                    role=row[3],
                    bio=row[4],
                    first_name=row[5],
                    last_name=row[6],
                )
            print('Данные пользователей загружены в БД!')
        file_path = settings.STATICFILES_DIRS[0] / 'data' / 'review.csv'
        with open(file_path, encoding='utf-8') as csv_file:
            reader_object = csv.reader(csv_file)
            next(reader_object)
            for row in reader_object:
                user = get_object_or_404(User, id=row[3])
                obj, created = Review.objects.get_or_create(
                    id=row[0],
                    title_id=row[1],
                    text=row[2],
                    author=user,
                    score=row[4],
                    pub_date=row[5],
                )
            print('Данные отзывов загружены в БД!')
        file_path = settings.STATICFILES_DIRS[0] / 'data' / 'comments.csv'
        with open(file_path, encoding='utf-8') as csv_file:
            reader_object = csv.reader(csv_file)
            next(reader_object)
            for row in reader_object:
                user = get_object_or_404(User, id=row[3])
                obj, created = Comment.objects.get_or_create(
                    id=row[0],
                    review_id=row[1],
                    text=row[2],
                    author=user,
                    pub_date=row[4],
                )
            print('Данные комментариев загружены в БД!')
