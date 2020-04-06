from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, authentication

schema_view = get_schema_view(
    openapi.Info(
        title='Your project API',
        default_version='v1',
        description='You can change src.app.utils.api_schema',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(authentication.BasicAuthentication, authentication.SessionAuthentication)
)
