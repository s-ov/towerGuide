import django_filters
from .models import Node

class NodeFilter(django_filters.FilterSet):

    class Meta:
        model = Node
        fields = {
            'slug': ['exact']
         }
