import datetime
import graphene

from graphene import Node
from graphene.types import Scalar
from graphql.language import ast

from django.utils import timezone


class StrDateTime(Scalar):
    """DateTime Scalar Description"""

    @staticmethod
    def serialize(dt):
        dtz = timezone.localtime(dt)
        return dtz.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return datetime.datetime.strptime(node.value, "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def parse_value(value):
        return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


class CustomNode(Node):
    id = graphene.ID(required=True)

    class Meta:
        name = "Node"

    @staticmethod
    def to_global_id(type, id):
        return id

    @staticmethod
    def get_node_from_global_id(info, global_id, only_type=None):
        # if cls not in only_type._meta.interfaces:
        #     return None

        get_node = getattr(only_type, "get_node", None)
        if get_node:
            return get_node(info, global_id)