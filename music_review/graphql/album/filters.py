import django_filters

from ...reviews.models import Album


class AlbumFilter(django_filters.FilterSet):
    performer__name = django_filters.CharFilter(lookup_expr="icontains")
    title = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Album
        fields = ["performer", "year"]
