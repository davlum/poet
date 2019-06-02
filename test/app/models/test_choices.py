import app.models.choices as choices
from django.test import TestCase


class TestChoices(TestCase):

    def test_validate_date(self):
        with self.assertRaises(ValueError):
            choices.validate_date('2222-22-22')

        with self.assertRaises(ValueError):
            choices.validate_date('not a date')

        with self.assertRaises(ValueError):
            choices.validate_date('2222-22')

        with self.assertRaises(ValueError):
            choices.validate_date('0000')

        self.assertIsNone(choices.validate_date('1991-05-03'))
        self.assertIsNone(choices.validate_date('1991-05'))
        self.assertIsNone(choices.validate_date('1991'))
        self.assertIsNone(choices.validate_date(None))
