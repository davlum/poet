from django.test import TestCase
from app.models.entity import Entity, EntityToEntityRel


class TestWorkModel(TestCase):
    fixtures = ['poet']

    def test_entity_stringify_default(self):
        entity = Entity()
        entity.id = 666
        entity.save()
        self.assertEqual(str(entity), 'Entidad 666')

    def test_entity_stringify_named(self):
        entity = Entity()
        title_string = 'title_string'
        entity.full_name = title_string
        entity.save()
        self.assertEqual(str(entity), title_string)

    def test_entity_rel_stringify(self):
        entity = EntityToEntityRel.objects.get(pk=1)
        self.assertEqual(str(entity), 'Relación de Frágil a Iraida Noriega')
