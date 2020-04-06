import graphene
from graphene import Field

from graphene_django.types import ErrorType
from graphene.types.base import BaseOptions

from django.core.exceptions import ObjectDoesNotExist


class DeleteMutationOptions(BaseOptions):
    model = None
    arguments = None
    output = None
    resolver = None
    interfaces = ()
    fields = None


class DeleteMutation(graphene.Mutation):
    class Meta:
        abstract = True
    id = graphene.ID()
    ok = graphene.Boolean(
        description="Boolean field that return mutation result request."
    )
    errors = graphene.List(ErrorType, description="Errors list for the field")

    class Arguments:
        id = graphene.ID(required=True)

    @classmethod
    def __init_subclass_with_meta__(
        cls,
        model=None,
        interfaces=(),
        resolver=None,
        output=None,
        arguments=None,
        _meta=None,
        **options
    ):
        if not _meta:
            _meta = DeleteMutationOptions(cls)

        assert model is not None, ("Model class in {} must be need.").format(
            cls.__name__
        )
        _meta.model = model
        super(DeleteMutation, cls).__init_subclass_with_meta__(
            interfaces=interfaces,
            resolver=resolver,
            output=output,
            arguments=arguments,
            _meta=_meta,
            **options
        )

    @classmethod
    def get_errors(cls, errors):
        errors_dict = {"ok": False, "errors": errors, "id": None}

        return cls(**errors_dict)

    @classmethod
    def perform_mutate(cls, obj, info):
        resp = {"ok": True, "errors": None, "id": obj.id}

        return cls(**resp)

    @classmethod
    def mutate(cls, root, info, id):
        try:
            obj = cls._meta.model.objects.get(id=id)
            obj.delete()
            obj.id = id
            return cls.perform_mutate(obj, info)
        except ObjectDoesNotExist:
            return cls.get_errors(
                [
                    ErrorType(
                        field="id",
                        messages=[
                            "A {} obj with id {} do not exist".format(
                                cls._meta.model.__name__, id
                            )
                        ],
                    )
                ]
            )

    @classmethod
    def Field(
        cls, name=None, description=None, deprecation_reason=None, required=False
    ):
        """ Mount instance of mutation Field. """
        return Field(
            cls._meta.output,
            args=cls._meta.arguments,
            resolver=cls._meta.resolver,
            name=name,
            description=description or cls._meta.description,
            deprecation_reason=deprecation_reason,
            required=required,
        )