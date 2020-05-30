from django.contrib.auth import get_user_model

from graphql_jwt.testcases import JSONWebTokenTestCase

CREATE_PERFORMER = """
mutation CreatePerformer {
  createPerformer(input: {
    name: "John Lennon",
  }) {
    performer {
      name
      id
      user {
         username
      }
    }
  }
}"""

READ_PERFORMER = """
query ReadPerformer($performer: ID!) {
  performer(id: $performer) {
    id
    name
    user {
      username
    }
  }
}
"""

UPDATE_PERFORMER = """
mutation UpdatePerformer($performer: ID!, $name: String) {
  updatePerformer(input: {
    performer: $performer,
    name: $name,
  }) {
    performer {
      name
      id
    }
  }
}"""

DELETE_PERFORMER = """
mutation DeletePerformer($performer: ID!) {
  deletePerformer(input: {
    performer: $performer,
  }) {
    success
  }
}"""


class PerformerSuccessTests(JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username="test")
        self.client.authenticate(self.user)

    def create_performer(self):
        result = self.client.execute(CREATE_PERFORMER)
        return result.data["createPerformer"]["performer"]["id"]

    def test_create_performer(self):
        result = self.client.execute(CREATE_PERFORMER)
        self.assertIsNone(result.errors)
        performer_id = result.data["createPerformer"]["performer"]["id"]
        self.assertEqual(
            result.data["createPerformer"]["performer"]["user"]["username"], "test"
        )
        result = self.client.execute(READ_PERFORMER, {"performer": performer_id})
        self.assertIsNone(result.errors)
        self.assertEqual(result.data["performer"]["user"]["username"], "test")

    def test_update_performer(self):
        performer_id = self.create_performer()
        new_name = "YOKO"
        result = self.client.execute(
            UPDATE_PERFORMER, {"performer": performer_id, "name": new_name}
        )
        self.assertIsNone(result.errors)
        self.assertEqual(result.data["updatePerformer"]["performer"]["name"], new_name)
        result = self.client.execute(READ_PERFORMER, {"performer": performer_id})
        self.assertIsNone(result.errors)
        self.assertEqual(result.data["performer"]["name"], new_name)

    def test_delete_performer(self):
        performer_id = self.create_performer()
        result = self.client.execute(DELETE_PERFORMER, {"performer": performer_id})
        self.assertIsNone(result.errors)
        self.assertTrue(result.data["deletePerformer"]["success"])
        result = self.client.execute(READ_PERFORMER, {"performer": performer_id})
        self.assertIsNone(result.errors)
        self.assertIsNone(result.data["performer"])


class PerformerFailureTests(JSONWebTokenTestCase):
    def test_create_performer(self):
        result = self.client.execute(CREATE_PERFORMER)
        self.assertIsNotNone(result.errors)
        self.assertEqual(len(result.errors), 1)

    def test_delete_performer(self):
        result = self.client.execute(UPDATE_PERFORMER)
        self.assertIsNotNone(result.errors)
        self.assertEqual(len(result.errors), 1)

    def test_update_performer(self):
        result = self.client.execute(DELETE_PERFORMER)
        self.assertIsNotNone(result.errors)
        self.assertEqual(len(result.errors), 1)
