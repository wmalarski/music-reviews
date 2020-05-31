from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase

from music_review.reviews.models import Performer, Album, Review

READ_ALBUM_RANDOM_SET = """
query Random {
  randomAlbumSet(first: 5) {
    edges {
      node {
        id
      }
    }
  }
}
"""

READ_ALBUM_SET = """
query ReadAlbums($orderBy: String) {
  albumSet(orderBy: $orderBy) {
    edges {
      node {
        id
        year
      }
    }
  }
}
"""


class RandomAlbumTests(JSONWebTokenTestCase):
    def setUp(self):
        user = get_user_model().objects.create(username="test")
        self.client.authenticate(user)
        performer = Performer.objects.create(name="John Lennon")

        albums = []
        for a in range(20):
            album = Album.objects.create(
                performer=performer, title=str(a), year=1970 - a
            )
            albums.append(album)

        Review.objects.create(album=albums[0], user=user, review="", rating=5.5)
        Review.objects.create(album=albums[1], user=user, review="", rating=5.5)

    def test_read_random_albums(self):
        result = self.client.execute(READ_ALBUM_RANDOM_SET)
        self.assertIsNone(result.errors)
        random_ids1 = {
            edge["node"]["id"] for edge in result.data["randomAlbumSet"]["edges"]
        }
        result = self.client.execute(READ_ALBUM_RANDOM_SET)
        self.assertIsNone(result.errors)
        random_ids2 = {
            edge["node"]["id"] for edge in result.data["randomAlbumSet"]["edges"]
        }
        self.assertGreater(len(random_ids1.union(random_ids2)), 5)

    def test_read_albums_sort(self):
        result = self.client.execute(READ_ALBUM_SET, {"orderBy": "-year"})
        self.assertIsNone(result.errors)
        years = [edge["node"]["year"] for edge in result.data["albumSet"]["edges"]]
        self.assertTrue(all(year1 > year2 for year1, year2 in zip(years, years[1:])))
