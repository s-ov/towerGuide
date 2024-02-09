import django_filters
from .models import Node

class NodeFilter(django_filters.FilterSet):
    # name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Node
        fields = {
            'slug': ['icontains']
         }
