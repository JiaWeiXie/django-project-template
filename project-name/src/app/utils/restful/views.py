from rest_framework import viewsets, permissions


# Create your views here.
class EagerLoadingGenericViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        serializer_class = self.get_serializer_class()
        if hasattr(serializer_class, 'setup_eager_loading'):
            queryset = super().get_queryset()
            queryset = serializer_class.setup_eager_loading(queryset)
            return queryset
        return super().get_queryset()