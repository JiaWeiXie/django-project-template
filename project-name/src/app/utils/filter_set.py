from django_filters import FilterSet

from djangorestframework_camel_case.util import camel_to_underscore
from djangorestframework_camel_case.settings import api_settings

from django.http import QueryDict

json_underscoreize = api_settings.JSON_UNDERSCOREIZE


class UnderScoreizeFilterSet(FilterSet):
    def __init__(self, data=None, queryset=None, request=None, prefix=None):
        underscore_data = camel_to_underscore(data.urlencode(), **json_underscoreize)
        data = QueryDict(underscore_data)
        super().__init__(data=data, queryset=queryset, request=request, prefix=prefix)