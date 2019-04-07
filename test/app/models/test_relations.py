from django.test import TestCase
import app.models.relations as rel


class TestRelations(TestCase):

    def test_strip_to_none(self):
        result = rel.strip_to_none(None)
        self.assertIsNone(result)

        result = rel.strip_to_none('')
        self.assertIsNone(result)

        result = rel.strip_to_none('   ')
        self.assertIsNone(result)

        result = rel.strip_to_none(' hello   ')
        self.assertEqual('hello', result)
