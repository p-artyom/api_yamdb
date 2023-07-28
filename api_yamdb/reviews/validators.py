import re

from django.core.exceptions import ValidationError


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            'Имя пользователя не может быть <me>.',
            params={'value': value},
        )
    if not re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value):
        raise ValidationError(
            f'Не допустимые символы <{value}> в имени.',
            params={'value': value},
        )
