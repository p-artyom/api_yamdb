from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title, User


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('slug',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('slug',)
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description', 'category')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(
    User,
    list_display=(
        'username',
        'email',
        'role',
        'bio',
        'first_name',
        'last_name',
        'confirmation_code',
    ),
    search_fields=(
        'username',
        'role',
    ),
    list_filter=('username',),
    empty_value_display='-пусто-',
)

admin.site.register(Comment)
admin.site.register(Review)
