import django_filters

from ...reviews.models import Performer


class PerformerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Performer
        fields = ["name"]

    order_by = django_filters.OrderingFilter(
        fields=(
            ("name", "name"),
            ("created", "created"),
            ("last_updated", "last_updated"),
        )
    )
