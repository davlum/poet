from django.test import TestCase
import app.controllers.collection as col
from django.http import Http404


class TestCollectionController(TestCase):
    fixtures = ['poet']

    def test_get_collection_or_404(self):
        reference = {
            'album_art_design': None,
            'collection_name': 'Eslam de poesía 33 Rojo Córdova CCD',
            'commentary': 'Slam de poesía conducido por Rojo Córdova en el Centro de '
                          'Cultura Digital, CDMX, el 5 de diciembre de 2015.',
            'id': 315,
            'image': 'images/13/Eslam_CCD_Radio.jpg',
            'origin': 'Slam de poesía',
            'release_state': 'PUBLICADO'
        }
        result = col.get_collection_or_404(315)
        self.assertDictEqual(result, reference)

        with self.assertRaises(Http404):
            col.get_collection_or_404(1)

    def test_clean_collection(self):
        reference = {
            'album_art_design': None,
            'collection_name': 'Eslam de poesía 33 Rojo Córdova CCD',
            'commentary': '',
            'id': 315,
            'image': 'images/13/Eslam_CCD_Radio.jpg',
            'origin': 'Slam de poesía',
            'release_state': 'PUBLICADO'
        }
        result = col.clean_collection(reference)
        self.assertDictEqual(result, {
            'album_art_design': None,
            'collection_name': 'Eslam de poesía 33 Rojo Córdova CCD',
            'commentary': None,
            'id': 315,
            'collection_id': 315,
            'image': '/media/images/13/Eslam_CCD_Radio.jpg',
            'origin': 'Slam de poesía',
            'release_state': 'PUBLICADO'
        })

    def test_get_recordings(self):
        pass




