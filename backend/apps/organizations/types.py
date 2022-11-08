import graphene
from apps.organizations.models import Organization, OrganizationSettings
from apps.flows.types import FlowType
from apps.flows.models import Flow
from graphene_django.types import DjangoObjectType


class OrganizationType(DjangoObjectType):
    class Meta:
        model = Organization
        fields = "__all__"


class OrganizationSettingsType(DjangoObjectType):
    flows_in_organization = graphene.List(FlowType)

    def resolve_flows_in_organization(self, info):
        return Flow.objects.filter(organization=self.organization)

    class Meta:
        model = OrganizationSettings
        fields = "__all__"
