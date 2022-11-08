import graphene
from graphene_django.debug import DjangoDebug
from apps.organizations.mutations import CreateOrganization
from apps.organizations.types import OrganizationType, OrganizationSettingsType
from apps.organizations.models import Organization, OrganizationSettings


class Query(graphene.ObjectType):
    debug_organizations = graphene.Field(
        DjangoDebug, name='__debug_organizations')
    organizations_by_user = graphene.List(
        OrganizationType, description='Список организаций для конкретного пользователя')
    default_room_settings = graphene.Field(
        OrganizationSettingsType, subdomain=graphene.String(), description='Настроки по-умолчания для комнат в конкретной организации')

    def resolve_organizations_by_user(root, info, **kwargs):
        user = info.context.user
        return Organization.objects.filter(organization_owner=user).order_by('id')

    def resolve_default_room_settings(root, info, subdomain):
        try:
            user = info.context.user
            organization = Organization.objects.get(
                subdomain=subdomain)
            return OrganizationSettings.objects.get(organization=organization)
        except Exception as e:
            return None


class Mutation(graphene.ObjectType):
    create_organization = CreateOrganization.Field()
