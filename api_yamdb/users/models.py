from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRole(models.TextChoices):
    USER = 'user', 'Пользователь'
    MODERATOR = 'moderator', 'Модератор'
    ADMIN = 'admin', 'Администратор'


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=settings.USERNAME_MAX_LENGTH,
        unique=True,
        validators=[username_validator],
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    email = models.EmailField(
        verbose_name=_('email address'),
        max_length=settings.AUTH_MAX_LENGTH,
        unique=True,
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=settings.AUTH_MAX_LENGTH,
        blank=True,
        null=True,
        editable=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=settings.ROLE_MAX_LENGTH,
        choices=UserRole.choices,
        default=UserRole.USER,
    )

    @property
    def is_user(self):
        return self.role == UserRole.USER

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN or self.is_superuser

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('username',)
