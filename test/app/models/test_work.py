from django.test import TestCase
from app.models.work import WorkCollection, Work


class TestWorkModel(TestCase):
    fixtures = ['poet']

    def test_work_collection_stringify_default(self):
        work_collection = WorkCollection()
        work_collection.id = 666
        work_collection.save()
        self.assertEqual(str(work_collection), 'Serie 666')

    def test_work_collection_stringify_named(self):
        work_collection = WorkCollection()
        title_string = 'title_string'
        work_collection.collection_name = title_string
        work_collection.save()
        self.assertEqual(str(work_collection), title_string)

    def test_work_stringify_default(self):
        work = Work.objects.get(pk=1)
        self.assertEqual(str(work), 'La guerra es una locura extrema')
