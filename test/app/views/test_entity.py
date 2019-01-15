from django.test import TestCase
from django.http import Http404


class TestUtils(TestCase):
    fixtures = ['poet']

    def setUp(self):
        self.response = self.client.get('/collection/315')


    def test_status_code(self):
        self.assertEqual('', self.response.body)
        self.assertEqual(self.response.status_code, 200)

    def test_csrf(self):
        self.assertContains(self.response, 'csrf-token')

    def test_home_page_returns_correct_html(self):
        self.assertContains(self.response, 'search-form')
        self.assertTrue(self.response.content.startswith(b'<!DOCTYPE html>'))
        self.assertContains(self.response, 'POÉTICA<i>S</i>ONORA')
        self.assertTrue(self.response.content.endswith(b'</html>'))