from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError

from reviews.validators import validate_username

from api_yamdb.settings import MAX_LENGTH, MAX_LENGTH_NAME

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLE_CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]


class User(AbstractUser):
    username = models.CharField(
        validators=(validate_username,),
        max_length=MAX_LENGTH_NAME,
        unique=True,
        db_index=True,
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        db_index=True,
    )
    role = models.CharField(
        'роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True,
    )
    bio = models.TextField('биография', blank=True)
    first_name = models.CharField(
        'имя',
        max_length=MAX_LENGTH_NAME,
        blank=True
    )
    last_name = models.CharField(
        'фамилия',
        max_length=MAX_LENGTH_NAME,
        blank=True
    )
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=255,
        null=True,
        blank=False,
        default='XXXX',
    )

    def validate_confirmation_code(self, value):
        if value != self.confirmation_code:
            raise ValidationError('Неверный код подтверждения!')

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ('username',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField('название', max_length=MAX_LENGTH)
    slug = models.SlugField('ключ', unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField('название', max_length=MAX_LENGTH)
    slug = models.SlugField('ключ', unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField('название произведения', max_length=MAX_LENGTH)
    year = models.IntegerField('год выпуска')
    description = models.TextField('описание', blank=True)
    genre = models.ManyToManyField(
        Genre,
        verbose_name='ключ жанра',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='ключ категории',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('-year', 'name')
        default_related_name = 'titles'
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    author = author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор',
    )
    text = models.TextField(verbose_name='текст')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='произведение',
    )
    score = models.IntegerField(
        verbose_name='оценка',
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1),
        ],
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ['-pub_date']
        default_related_name = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title',
            ),
        )

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Ревью',
    )
    text = models.TextField(verbose_name='текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ['-pub_date']
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
