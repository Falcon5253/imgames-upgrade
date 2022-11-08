from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.users.models import User
from apps.users.forms import UserChangeForm, UserCreationForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    # Поля, которые используются при отображении модели пользователя.
    # Они переопределяют определения в базовом UserAdmin
    # которые ссылаются на определенные поля в auth.User.
    list_display = ['full_name', 'email']
    fieldsets = [
        ['Данные авторизации', {'fields': ['email', 'password']}],
        ['Личная информация', {'fields': [
            'last_name', 'first_name', 'avatar']}],
        ['Настройки', {'fields': ['groups', 'is_admin',
                                  'is_active', 'is_staff', 'is_superuser']}],
        ['Важные отметки времени', {
            'fields': ['last_login', 'registered_at']}],
    ]
    # add_fieldsets не является стандартным атрибутом ModelAdmin. UserAdmin
    # переопределяет get_fieldsets для использования этого атрибута при создании пользователя.
    add_fieldsets = [[None, {'classes': ['wide'], 'fields': [
        'email', 'first_name', 'last_name', 'password1', 'password2']}], ]
    search_fields = ['email']
    ordering = ['email']
    readonly_fields = ['last_login', 'registered_at']


# Регистрируем новый UserAdmin
admin.site.register(User, UserAdmin)
# Отключаем модель Group для админпанели.
# admin.site.register(Group)
