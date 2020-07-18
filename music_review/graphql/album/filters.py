import random

import django_filters

from ...reviews.models import Album, Review


class AlbumFilter(django_filters.FilterSet):
    performer__name = django_filters.CharFilter(lookup_expr="icontains")
    name = django_filters.CharFilter(lookup_expr="icontains")
    year__gt = django_filters.NumberFilter(field_name="year", lookup_expr="gt")
    year__lt = django_filters.NumberFilter(field_name="year", lookup_expr="lt")

    class Meta:
        model = Album
        fields = ["performer", "year"]

    order_by = django_filters.OrderingFilter(
        fields=(
            ("year", "year"),
            ("created", "created"),
            ("last_updated", "last_updated"),
        )
    )


class RandomAlbumFilter(django_filters.FilterSet):
    year__gt = django_filters.NumberFilter(field_name="year", lookup_expr="gt")
    year__lt = django_filters.NumberFilter(field_name="year", lookup_expr="lt")

    class Meta:
        model = Album
        fields = ["year"]

    @property
    def qs(self):
        reviewed = Review.objects.values_list("album", flat=True).distinct()
        qs = super().qs.exclude(id__in=reviewed)
        result = list(qs)
        random.shuffle(result)
        return result
