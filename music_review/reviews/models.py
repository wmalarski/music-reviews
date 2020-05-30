from django.contrib.auth import get_user_model
from django.db import models


class Performer(models.Model):
    """

    """

    name = models.TextField()
    logo_url = models.TextField(null=True)
    description = models.TextField(default="")
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)


class Album(models.Model):
    """

    """

    performer = models.ForeignKey(Performer, on_delete=models.CASCADE)
    title = models.TextField()
    year = models.IntegerField()
    cover_url = models.TextField(null=True)
    description = models.TextField(default="")
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)


class Review(models.Model):
    """

    """

    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
