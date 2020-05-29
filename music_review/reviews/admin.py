from django.contrib import admin

from .models import Album, Review, Performer

admin.site.register(Album)
admin.site.register(Review)
admin.site.register(Performer)
