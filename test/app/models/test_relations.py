from django.test import TestCase
from app.models.relations import strip_to_none


class TestRelations(TestCase):

    def test_strip_to_none(self):
        result = strip_to_none(None)
        self.assertIsNone(result)

        result = strip_to_none('')
        self.assertIsNone(result)

        result = strip_to_none('   ')
        self.assertIsNone(result)

        result = strip_to_none(' hello   ')
        self.assertEqual('hello', result)
