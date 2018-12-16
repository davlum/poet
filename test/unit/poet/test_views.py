from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from app.views import index


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = index(request)
        self.assertTrue(response.content.startswith(b'<!DOCTYPE html>'))
        self.assertInHTML('<h1><b>POÉTICA<i>S</i>ONORA</b></h1>', response.content.decode())
        self.assertTrue(response.content.endswith(b'</html>'))