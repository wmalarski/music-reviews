from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase
from graphql_relay import to_global_id

from music_review.reviews.models import Performer, Album

CREATE_REVIEW = """
mutation CreateReview($album: ID!) {
  createReview(input: {
    album: $album
    review: "Ou My"
    rating: 8.5
  }) {
    review {
      id
      album {
        id
      }
      review
      rating
      user {
        username
      }
    }
  }
}"""

READ_REVIEW = """
query ReadReview($review: ID!) {
  review(id: $review) {
    id
    album {
      id
    }
    review
    rating
    user {
      username
    }
  }
}
"""

UPDATE_REVIEW = """
mutation UpdateReview($id: ID!, $review: String) {
  updateReview(input: {
    reviewId: $id
    review: $review
  }) {
    review {
      review
    }
  }
}"""

DELETE_ALBUM = """
mutation DeleteReview($review: ID!) {
  deleteReview(input: {
    review: $review,
  }) {
    success
  }
}"""


class ReviewSuccessTests(JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username="test")
        self.performer = Performer.objects.create(name="John Lennon")
        self.album = Album.objects.create(
            performer=self.performer, title="John Lennon Band", year=1970
        )
        self.album_id = to_global_id("AlbumType", self.album.id)
        self.client.authenticate(self.user)

    def create_review(self):
        result = self.client.execute(CREATE_REVIEW, {"album": self.album_id})
        return result.data["createReview"]["review"]["id"]

    def test_create_review(self):
        result = self.client.execute(CREATE_REVIEW, {"album": self.album_id})
        self.assertIsNone(result.errors)
        review_id = result.data["createReview"]["review"]["id"]
        self.assertEqual(
            result.data["createReview"]["review"]["user"]["username"], "test"
        )
        self.assertEqual(
            result.data["createReview"]["review"]["album"]["id"], self.album_id
        )
        result = self.client.execute(READ_REVIEW, {"review": review_id})
        self.assertIsNone(result.errors)
        self.assertEqual(result.data["review"]["user"]["username"], "test")
        self.assertEqual(result.data["review"]["album"]["id"], self.album_id)

    def test_update_review(self):
        review_id = self.create_review()
        new_review = "YOKO"
        result = self.client.execute(
            UPDATE_REVIEW, {"id": review_id, "review": new_review}
        )
        self.assertIsNone(result.errors)
        self.assertEqual(result.data["updateReview"]["review"]["review"], new_review)
        result = self.client.execute(READ_REVIEW, {"review": review_id})
        self.assertIsNone(result.errors)
        self.assertEqual(result.data["review"]["review"], new_review)

    def test_delete_review(self):
        review_id = self.create_review()
        result = self.client.execute(DELETE_ALBUM, {"review": review_id})
        self.assertIsNone(result.errors)
        self.assertTrue(result.data["deleteReview"]["success"])
        result = self.client.execute(READ_REVIEW, {"review": review_id})
        self.assertIsNone(result.errors)
        self.assertIsNone(result.data["review"])


class ReviewFailureTests(JSONWebTokenTestCase):
    def test_create_review(self):
        result = self.client.execute(CREATE_REVIEW)
        self.assertIsNotNone(result.errors)
        self.assertEqual(len(result.errors), 1)

    def test_delete_review(self):
        result = self.client.execute(UPDATE_REVIEW)
        self.assertIsNotNone(result.errors)
        self.assertEqual(len(result.errors), 1)

    def test_update_review(self):
        result = self.client.execute(DELETE_ALBUM)
        self.assertIsNotNone(result.errors)
        self.assertEqual(len(result.errors), 1)
