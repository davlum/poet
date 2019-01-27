from django.test import TestCase
from django.http import Http404


class TestCollection(TestCase):
    fixtures = ['poet']

    def setUp(self):
        self.response = self.client.get('/coleccion/315')

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_csrf(self):
        self.assertContains(self.response, 'csrf-token')

    def test_entity_contains_search(self):
        self.assertContains(self.response, 'search-form')

    def test_entity_contains_audio(self):
        self.assertContains(self.response, 'wavesurfer-container')
