from django.contrib.auth import get_user_model
from django.db import models


class Performer(models.Model):
    """

    """

    name = models.TextField()
    logo_url = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(auto_created=True)
    last_updated = models.DateTimeField(auto_now=True)


class Album(models.Model):
    """

    """

    performer = models.ForeignKey(Performer, on_delete=models.CASCADE)
    title = models.TextField()
    year = models.IntegerField()
    cover_url = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(auto_created=True)
    last_updated = models.DateTimeField(auto_now=True)


class Review(models.Model):
    """

    """

    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.FloatField()
    created = models.DateTimeField(auto_created=True)
    last_updated = models.DateTimeField(auto_now=True)
