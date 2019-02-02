from django.test import TestCase
import app.controllers.search as search
from collections import defaultdict


class TestSearchController(TestCase):
    fixtures = ['poet']

    def test_make_tsvector(self):
        result = search.make_tsvector(search.CITIES_FIELDS)
        self.assertEqual(result, "setweight(to_tsvector('es', coalesce(city::text,'')), 'A') || "
                                 "setweight(to_tsvector('es', coalesce(country::text,'')), 'A')")

    def test_field_search(self):
        result = search.make_field_search(3)
        self.assertEqual(result, "to_tsquery('es', CONCAT(CONCAT(%s, ':*'), ' | ', "
                                 "CONCAT(%s, ':*'), ' | ', CONCAT(%s, ':*')))")

    def test_search_work(self):
        result = search.make_query(search.SEARCH_WORKS, [], '   ')
        self.assertListEqual(result, [])

        result = search.make_query(search.SEARCH_WORKS, search.WORK_FIELDS, 'che')
        self.assertEqual(len(result), 3)

    def test_collection_counter(self):
        d = {
            1: {
                'count': 2,
                'name': 'hello'
            }
        }
        result = search.collection_counter(d, 1, 'hmmm')
        self.assertDictEqual(result, {
            1: {
                'count': 3,
                'name': 'hello'
            }
        })
        # reset mutable d
        d = {
            1: {
                'count': 2,
                'name': 'hello'
            }
        }
        result = search.collection_counter(d, 2, 'hmmm')
        self.assertDictEqual(result, {
            1: {
                'count': 2,
                'name': 'hello'
            },
            2: {
                'count': 1,
                'name': 'hmmm'
            }
        })

    def test_dict_agg(self):
        d = defaultdict(int)
        d['hello'] = 2

        result = search.dict_agg(d, 'hello')
        self.assertDictEqual(result, {'hello': 3})

        d = defaultdict(int)
        d['hello'] = 2

        result = search.dict_agg(d, 'hi')
        self.assertDictEqual(result, {'hello': 2, 'hi': 1})

    def test_aggregate_data(self):
        inp = [{


            }
        ]