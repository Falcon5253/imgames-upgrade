from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from apps.users.models import User


class UserCreationForm(forms.ModelForm):
    """
    Форма для создания новых пользователей.
    Включает все обязательные поля, а также повторный пароль
    """
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean_password2(self):
        # Проверяем, что две записи пароля совпадают
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают!")
        return password2

    def save(self, commit=True):
        # Сохраняем предоставленный пароль в хешированном формате
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    Форма для обновления пользователей. Включает в себя все поля на
    пользователя, но заменяет поле пароля на админ
    поле отображения хэша пароля.
    """
    help_text = """Необработанные пароли не сохраняются, поэтому нет возможности увидеть пароль этого пользователя,
                   но вы можете изменить пароль, используя <a href="../password/">эту форму</a>."""
    password = ReadOnlyPasswordHashField(label='Пароль', help_text=help_text)

    class Meta:
        model = User
        fields = ['email', 'password', 'is_active', 'is_admin']

    def clean_password(self):
        # Независимо от того, что предоставил пользователь, вернёт начальное значение.
        # Это делается здесь, а не на поле, потому что
        # поле не имеет доступа к начальному значению
        return self.initial["password"]
