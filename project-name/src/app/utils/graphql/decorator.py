from functools import wraps

from graphql.execution.base import ResolveInfo

from rest_framework import exceptions
from rest_framework.settings import api_settings


def context(f):
    def decorator(func):
        def wrapper(*args, **kwargs):
            info = next(arg for arg in args if isinstance(arg, ResolveInfo))
            return func(info.context, *args, **kwargs)
        return wrapper
    return decorator


class PermissionHandler:
    def __init__(self, func, permission_classes=api_settings.DEFAULT_PERMISSION_CLASSES):
        self.target_func = func
        self.permission_classes = permission_classes

    def permission_denied(self, request, message=None):
        """
        If request is not permitted, determine what kind of exception to raise.
        """
        func_name = self.target_func.__name__
        field_name = str(func_name).split('resolve_')[-1] or func_name
        message = f"You do not have permission to perform {field_name}." if message is None else message
        if request.authenticators and not request.successful_authenticator:
            raise exceptions.NotAuthenticated()
        raise exceptions.PermissionDenied(detail=message)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        return [permission() for permission in self.permission_classes]

    def check_permissions(self, request):
        """
        Check if the request should be permitted.
        Raises an appropriate exception if the request is not permitted.
        """
        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied(
                    request, message=getattr(permission, 'message', None)
                )


def rest_permission(permission_classes=api_settings.DEFAULT_PERMISSION_CLASSES):
    """
    # NOTICE: Not support object-level permission.
    class UserNode(DjangoObjectType):
        @rest_permission([permissions.IsAdminUser])
        def resolve_is_superuser(parent, info):
            return parent.is_superuser
    """
    def decorator(f):
        permission_handler = PermissionHandler(f, permission_classes)
        @wraps(f)
        @context(f)
        def wrapper(context, *args, **kwargs):
            permission_handler.check_permissions(context)
            return f(*args, **kwargs)
        return wrapper
    return decorator

