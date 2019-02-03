from django.test import TestCase


class TestSearch(TestCase):
    fixtures = ['poet']

    def setUp(self):
        self.response = self.client.get('/buscar/?term=che&filter=works')

    def test_200_search(self):
        self.assertEqual(self.response.status_code, 200)

    def test_csrf(self):
        self.assertContains(self.response, 'csrf-token')

    def test_entity_contains_search(self):
        self.assertContains(self.response, 'search-form')

    def test_entity_contains_audio(self):
        self.assertContains(self.response, 'wavesurfer-container')
