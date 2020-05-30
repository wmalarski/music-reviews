from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase
from graphql_relay import to_global_id

from music_review.reviews.models import Performer

CREATE_ALBUM = """
mutation CreateAlbum($performer: ID!) {
  createAlbum(input: {
    performer: $performer
    title: "Yoko Ono Band"
    year: 1970
  }) {
    album {
      id
      performer {
        name
      }
      title
      year
      user {
        username
      }
    }
  }
}"""

READ_ALBUM = """
query ReadAlbum($album: ID!) {
  album(id: $album) {
    id
    performer {
      name
    }
    title
    year
    user {
      username
    }
  }
}
"""

UPDATE_ALBUM = """
mutation UpdateAlbum($album: ID!, $title: String) {
  updateAlbum(input: {
    album: $album
    title: $title
  }) {
    album {
      title
    }
  }
}"""

DELETE_ALBUM = """
mutation DeleteAlbum($album: ID!) {
  deleteAlbum(input: {
    album: $album,
  }) {
    success
  }
}"""


class AlbumSuccessTests(JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username="test")
        self.performer = Performer.objects.create(name="John Lennon")
        self.performer_id = to_global_id("PerformerType", self.performer.id)
        self.client.authenticate(self.user)

    def create_album(self):
        result = self.client.execute(CREATE_ALBUM, {"performer": self.performer_id})
        return result.data["createAlbum"]["album"]["id"]

    def test_create_album(self):
        result = self.client.execute(CREATE_ALBUM, {"performer": self.performer_id})
        self.assertIsNone(result.errors)
        album_id = result.data["createAlbum"]["album"]["id"]
        self.assertEqual(
            result.data["createAlbum"]["album"]["user"]["username"], "test"
        )
        self.assertEqual(
            result.data["createAlbum"]["album"]["performer"]["name"],
            self.performer.name,
        )
        result = self.client.execute(READ_ALBUM, {"album": album_id})
        self.assertIsNone(result.errors)
        self.assertEqual(result.data["album"]["user"]["username"], "test")
        self.assertEqual(result.data["album"]["performer"]["name"], self.performer.name)

    def test_update_album(self):
        album_id = self.create_album()
        new_title = "YOKO"
        result = self.client.execute(
            UPDATE_ALBUM, {"album": album_id, "title": new_title}
        )
        self.assertIsNone(result.errors)
        self.assertEqual(result.data["updateAlbum"]["album"]["title"], new_title)
        result = self.client.execute(READ_ALBUM, {"album": album_id})
        self.assertIsNone(result.errors)
        self.assertEqual(result.data["album"]["title"], new_title)

    def test_delete_album(self):
        album_id = self.create_album()
        result = self.client.execute(DELETE_ALBUM, {"album": album_id})
        self.assertIsNone(result.errors)
        self.assertTrue(result.data["deleteAlbum"]["success"])
        result = self.client.execute(READ_ALBUM, {"album": album_id})
        self.assertIsNone(result.errors)
        self.assertIsNone(result.data["album"])


class AlbumFailureTests(JSONWebTokenTestCase):
    def test_create_album(self):
        result = self.client.execute(CREATE_ALBUM)
        self.assertIsNotNone(result.errors)
        self.assertEqual(len(result.errors), 1)

    def test_delete_album(self):
        result = self.client.execute(UPDATE_ALBUM)
        self.assertIsNotNone(result.errors)
        self.assertEqual(len(result.errors), 1)

    def test_update_album(self):
        result = self.client.execute(DELETE_ALBUM)
        self.assertIsNotNone(result.errors)
        self.assertEqual(len(result.errors), 1)
