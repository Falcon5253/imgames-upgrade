import graphene
import graphql_jwt
from datetime import timezone
from graphene_django import DjangoObjectType
from uuid import uuid4

from django.contrib.auth import logout
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from apps.users.models import User
from graphql_jwt.decorators import login_required
from datetime import datetime
from config.settings import GRAPHQL_JWT


def jwt_payload(user, context=None):
    username = user.get_username()
    return {user.USERNAME_FIELD: username, 'user_id': user.id, 'email': user.email, 'exp': datetime.now(timezone.utc) + GRAPHQL_JWT['JWT_EXPIRATION_DELTA']}


class UserType(DjangoObjectType):
    """ Тип объекта User """

    class Meta:
        model = User
        only_fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'registered_at',
        ]


class Query(object):
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    users = graphene.List(UserType)
    profile = graphene.Field(UserType)

    @staticmethod
    @login_required
    def resolve_user(cls, info, **kwargs):
        return User.objects.get(id=kwargs.get('id'))

    @staticmethod
    def resolve_users(cls, info, **kwargs):
        return User.objects.all()

    @staticmethod
    def resolve_profile(cls, info, **kwargs):
        if info.context.user.is_authenticated:
            return info.context.user


class Register(graphene.Mutation):
    """ Мутация для регистрации нового пользователя """
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)

    def mutate(self, info, email, password, first_name, last_name):
        if User.objects.filter(email__iexact=email).exists():
            errors = ['emailAlreadyExists']
            return Register(success=False, errors=errors)

        # создаём пользователя
        user = User.objects.create(
            email=email,
            last_name=last_name,
            first_name=first_name,
        )
        user.set_password(password)
        user.save()
        return Register(success=True)


class Logout(graphene.Mutation):
    """ Мутация чтобы разлогинить пользователя """
    success = graphene.Boolean()

    def mutate(self, info):
        logout(info.context)
        return Logout(success=True)


class ResetPassword(graphene.Mutation):
    """ Мутация для запроса сброса пароля по email """
    success = graphene.Boolean()

    class Arguments:
        email = graphene.String(required=True)

    def mutate(self, info, email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            errors = ['emailDoesNotExists']
            return ResetPassword(success=False, errors=errors)

        params = {
            'user': user,
            'DOMAIN': settings.DOMAIN,
        }
        send_mail(
            subject='Password reset',
            message=render_to_string('mail/password_reset.txt', params),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )
        return ResetPassword(success=True)


class ResetPasswordConfirm(graphene.Mutation):
    """ Мутация для обновления пароля через ссылку в письме """
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    class Arguments:
        token = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, token, password):
        try:
            user = User.objects.get(token=token)
        except User.DoesNotExist:
            errors = ['wrongToken']
            return ResetPasswordConfirm(success=False, errors=errors)

        user.set_password(password)
        user.token = uuid4()
        user.save()
        return ResetPasswordConfirm(success=True)


class Mutation(object):
    login = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    register = Register.Field()
    logout = Logout.Field()
    delete_token_cookie = graphql_jwt.DeleteJSONWebTokenCookie.Field()
    reset_password = ResetPassword.Field()
    reset_password_confirm = ResetPasswordConfirm.Field()
