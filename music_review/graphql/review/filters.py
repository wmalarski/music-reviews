import django_filters

from ...reviews.models import Review


class ReviewFilter(django_filters.FilterSet):
    user__username = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Review
        fields = ["album", "user", "rating"]
