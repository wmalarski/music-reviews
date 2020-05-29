import django_filters

from ...reviews.models import Performer


class PerformerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Performer
        fields = ["name"]
