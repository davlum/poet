from django.test import TestCase


class HomePageTest(TestCase):

    def setUp(self):
        self.response = self.client.get('/')

    def test_csrf(self):
        self.assertContains(self.response, 'csrf-token')

    def test_home_page_returns_correct_html(self):
        self.assertTrue(self.response.content.startswith(b'<!DOCTYPE html>'))
        self.assertContains(self.response, 'POÉTICA<i>S</i>ONORA')
        self.assertTrue(self.response.content.endswith(b'</html>'))


