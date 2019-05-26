from django.test import TestCase
from app.models.work import Work, WorkCollection
from django.core.exceptions import ValidationError


class TestWorkModel(TestCase):
    # fixtures = ['poet']

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

    def test_work_validate_audio(self):
        work = Work()
        # work.id = 666
        with self.assertRaises(ValidationError):
            work.save()

        work.audio = 'not null'
        work.save()
