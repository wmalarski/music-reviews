import random

import django_filters

from ...reviews.models import Album, Review


class AlbumFilter(django_filters.FilterSet):
    performer__name = django_filters.CharFilter(lookup_expr="icontains")
    title = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Album
        fields = ["performer", "year"]

    order_by = django_filters.OrderingFilter(
        fields=(
            ("title", "title"),
            ("year", "year"),
            ("created", "created"),
            ("last_updated", "last_updated"),
        )
    )


class RandomAlbumFilter(django_filters.FilterSet):
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
