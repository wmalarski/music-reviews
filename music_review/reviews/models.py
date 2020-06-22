from django.contrib.auth import get_user_model
from django.db import models


class DateFieldsModel(models.Model):
    """

    """

    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)


class Performer(DateFieldsModel):
    """

    """

    name = models.TextField()
    mbid = models.TextField(unique=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)


class Album(DateFieldsModel):
    """

    """

    mbid = models.TextField(unique=True)
    performer = models.ForeignKey(Performer, on_delete=models.CASCADE)
    name = models.TextField()
    year = models.IntegerField()
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)


class Review(DateFieldsModel):
    """

    """

    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.FloatField()
