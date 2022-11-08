from uuid import uuid4

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(
            self,
            email,
            password,
            is_staff,
            is_superuser,
            **extra_fields):
        """
        Создаёт и сохраняет Пользователя с данными логином, email и паролем.
        """
        user = self.model(email=self.normalize_email(email),
                          is_active=True,
                          is_staff=is_staff,
                          is_superuser=is_superuser,
                          last_login=timezone.now(),
                          registered_at=timezone.now(),
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        is_staff = extra_fields.pop('is_staff', False)
        is_superuser = extra_fields.pop('is_superuser', False)
        return self._create_user(
            email,
            password,
            is_staff,
            is_superuser,
            **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(
            email,
            password,
            is_staff=True,
            is_superuser=True,
            **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        max_length=255)
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=30,
        default='Имя')
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=30,
        default='Фамилия')
    avatar = models.ImageField(verbose_name='Аватар', blank=True)
    token = models.UUIDField(
        verbose_name='Токен',
        default=uuid4,
        editable=False)

    is_admin = models.BooleanField(verbose_name='Администратор', default=False)
    is_active = models.BooleanField(verbose_name='Активирован', default=True)
    is_staff = models.BooleanField(
        verbose_name='Работник компании', default=False)
    registered_at = models.DateTimeField(
        verbose_name='Зарегистрирован',
        auto_now_add=timezone.now)

    # Настройки полей
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        verbose_name = 'сущность `Пользователь`'
        verbose_name_plural = 'Пользователи'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    full_name.fget.short_description = 'Имя и фамилия'

    @property
    def short_name(self):
        return f'{self.last_name} {self.first_name[0]}.'
    short_name.fget.short_description = 'Имя'

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.short_name

    def __str__(self):
        return f'{self.full_name} (#{str(self.pk)})'
