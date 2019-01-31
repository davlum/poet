from django.test import TestCase


class TestSearch(TestCase):
    fixtures = ['poet']

    def setUp(self):
        self.empty_search = self.client.get('/buscar/')

    def test_200_collection(self):
        self.assertEqual(self.empty_search.status_code, 200)

    def test_csrf(self):
        self.assertContains(self.empty_search, 'csrf-token')

    def test_entity_contains_search(self):
        self.assertContains(self.empty_search, 'search-form')
