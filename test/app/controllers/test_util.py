from django.test import TestCase
from unittest.mock import ANY
import app.controllers.util as u
from django.http import Http404


class TestUtils(TestCase):
    fixtures = ['poet']

    def test_query(self):
        result = {
            'id': 1,
            'full_name': 'La guerra es una locura extrema',
            'alt_name': None,
            'city': 'Ciudad de México, Distrito Federal',
            'country': 'México',
            'audio': 'audio/44/44/00014_JorgeReyes_LaGuerraEsUnaLocuraExtrema_2003_FONA_RAED_4.mp3',
            'tags': ['Radioarte', 'Poesía sonora', 'Arte sonoro', 'guerra', 'ruido', 'voz', 'repetición'],
            'commentary': ANY,
            'release_state': 'PUBLICADO',
            'copyright': '(C) Copyright',
            'copyright_country': 'México',
            'date_contributed': '2016-11-16',
            'date_digitalized': '2003-04-27',
            'date_published': '2003-04-27',
            'date_recorded': '2003-04-27',
            'languages': ['Español'],
            'media_of_origin': 'Digital',
            'track_number': 14,
            'in_collection': 325,
            'waveform_peaks': ANY,
            'poetry_text': None,
            'external_url': None}
        self.assertDictEqual(result, u.query('SELECT * FROM poet_work WHERE id = %s', [1])[0])

    def test_get_extension(self):
        self.assertEqual(u.get_extension('song.wav'), 'wav')

    def test_return_or_404(self):
        def raises():
            return [][0]

        with self.assertRaises(Http404):
            u.return_or_404(raises)

        def doesnt_raise():
            return ['woop'][0]

        self.assertEqual(u.return_or_404(doesnt_raise), 'woop')

    def test_normalize(self):
        result = u.normalize([1, -2, 4])
        self.assertListEqual(result, [0.25, -0.5, 1])

    def test_sort_entities(self):
