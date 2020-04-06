import graphene

from graphene_django.filter import DjangoFilterConnectionField


class Query(graphene.ObjectType):
    class Meta:
        description = "GraphQL Query API"


class Mutation:
    class Meta:
        description = "GraphQL Mutation API"


schema = graphene.Schema(query=Query, mutation=Mutation)